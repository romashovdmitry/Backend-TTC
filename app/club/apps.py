from django.apps import AppConfig


class ClubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club'

    # FIXME: можно убрать в будущем, если не понадобится по итогу
    def ready(self) -> None:
        """ signals initialization """
        # https://stackoverflow.com/a/21612050/24040439
        import club.signals
        return super().ready()
