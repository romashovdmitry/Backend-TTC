# python imports
import json
import logging

# ASGI Websocket imports
from channels.generic.websocket import AsyncWebsocketConsumer

# import custom foos, classes


logger = logging.getLogger(__name__)


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
        #     "second_player_score": 0
        # }
        # import custom foos, classes, etc
        from .db_actions import add_game_result
        from tournament.services import is_tournament_group_stage_finished
        return_json_dict = {
            "status": None,
            "tournament_status": None
        }

        try:
            text_data_json = json.loads(text_data)
            result_bool = await add_game_result(
                game_pk=text_data_json.get("game_pk"),
                first_player_score=text_data_json.get("first_player_score"),
                second_player_score=text_data_json.get("second_player_score")
            )

            rrrr = await is_tournament_group_stage_finished(text_data_json.get("game_pk"))

            if result_bool:
                await self.send(text_data=json.dumps({
                    "status": 200,
                    "is_tournament_finished": await is_tournament_group_stage_finished(text_data_json.get("game_pk"))
                }))

            else:
                await self.send(text_data=json.dumps({
                    "status": 400
                }))

        except Exception as ex:
            logger.error(
                f'GameResultConsumer.receive: {str(ex)}'
            )
            await self.send(text_data=json.dumps({
                "status": 400
            }))

    async def send_message(self, event):
        """
        Send message to frontend.
        """
        message = 'lol kek'

        await self.send(text_data=message)

    async def disconnect(self, close_code):
        """ Disconnect from websocket-connection """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )