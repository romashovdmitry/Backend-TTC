# python imports
import json
import logging

# ASGI Websocket imports
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


def token_get_user(validated_token):
    from rest_framework_simplejwt.authentication import JWTAuthentication
    from user.models import ClubAdmin
    jwt_auth = JWTAuthentication()
    user = jwt_auth.get_user(validated_token)

    return ClubAdmin.objects.filter(user=user).exists()


class GameResultConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Connect to backend websocket.
        """
        self.room_name = 'game'
        self.room_group_name = f'game_{self.room_name}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        # ожидается формат такой:
        # {
        #     "game_pk: 1,
        #     "first_player_score": 2,
        #     "second_player_score": 0,
        #     "access_token": "sdfsdfsdfsd..."
        # }
        # DRF imports
        from rest_framework_simplejwt.tokens import Token
        from rest_framework_simplejwt.authentication import JWTAuthentication
        # ASGI imports
        from asgiref.sync import sync_to_async
        # import custom foos, classes, etc
        from .db_actions import add_game_result
        from tournament.services import is_tournament_group_stage_finished

        return_json_dict = {
            "status": None,
            "tournament_status": None
        }

        try:
            jwt_auth = JWTAuthentication()
            access_token = json.loads(text_data).get("access_token")
            validated_token = jwt_auth.get_validated_token(access_token)
            user = await sync_to_async(token_get_user)(validated_token)

            if not user:
                await self.send(text_data=json.dumps({
                    "error": "user is not valid"
                }))

            text_data_json = json.loads(text_data)
            result_bool = await add_game_result(
                game_pk=text_data_json.get("game_pk"),
                first_player_score=text_data_json.get("first_player_score"),
                second_player_score=text_data_json.get("second_player_score")
            )

            if result_bool:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "status": 200,
                        "is_tournament_finished": await is_tournament_group_stage_finished(text_data_json.get("game_pk"))
                    }
                )

            else:
                await self.send(text_data=json.dumps({
                    "status": 400
                }))

        except Exception as ex:

            logger.error(
                f'GameResultConsumer.receive: {str(ex)}'
            )

            if "token_not_valid" in str(ex):
                await self.send(text_data=json.dumps({
                    "status": 401,

                }))

            else:

                await self.send(text_data=json.dumps({
                    "status": 400
                }))

    async def disconnect(self, close_code):
        """ Disconnect from websocket-connection """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


class KnockoutResultConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Connect to backend websocket. 
        """
        self.room_name = 'knock_game'
        self.room_group_name = f'knock_game_{self.room_name}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        # ожидается формат такой:
        # {
        #     "game_pk: 1,
        #     "first_player_score": 2,
        #     "second_player_score": 0,
        #     "access_token": "sdfsdfsdfsd..."
        # }
        # DRF imports
        from rest_framework_simplejwt.tokens import Token
        from rest_framework_simplejwt.authentication import JWTAuthentication
        # ASGI imports
        from asgiref.sync import sync_to_async
        # import custom foos, classes, etc
        from .db_actions import add_knock_game_result, create_knock_game_result

        try:
            jwt_auth = JWTAuthentication()
            access_token = json.loads(text_data).get("access_token")
            validated_token = jwt_auth.get_validated_token(access_token)
            user = await sync_to_async(token_get_user)(validated_token)

            if not user:
                await self.send(text_data=json.dumps({
                    "error": "user is not valid"
                }))

            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == "send_score":
                result_bool = await add_knock_game_result(
                    game_pk=text_data_json.get("game_pk"),
                    first_player_score=text_data_json.get("first_player_score"),
                    second_player_score=text_data_json.get("second_player_score")
                )
                if result_bool:

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "providerToStore",
                            "data": {
                                "status": 200,
                            }
                        }
                    )

                else:
                    await self.send(text_data=json.dumps({
                        "status": 400
                    }))

            else:
                result_bool = await create_knock_game_result(
                    tournament_pk=text_data_json.get("tournament_pk"),
                    first_player_pk=text_data_json.get("first_player_pk"),
                    second_player_pk=text_data_json.get("second_player_pk"),
                    horizontal_order=text_data_json.get("horizontal_order"),
                    vertical_order=text_data_json.get('vertical_order'),
                )

                if result_bool:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "providerToStore",
                            "data": {
                                "status": 200,
                            }
                        }
                    )

                else:
                    await self.send(text_data=json.dumps({
                        "status": 400
                    }))

        except Exception as ex:

            logger.error(
                f'KnockoutResultConsumer.receive: {str(ex)}'
            )

            if "token_not_valid" in str(ex):
                await self.send(text_data=json.dumps({
                    "status": 401,

                }))

            else:

                await self.send(text_data=json.dumps({
                    "status": 400
                }))

    async def providerToStore(self, event):
        """
        Обработка сообщений типа 'providerToStore'.
        """
        # Отправка данных обратно клиенту
        await self.send(text_data=json.dumps(event["data"]))


    async def disconnect(self, close_code):
        """ Disconnect from websocket-connection """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
