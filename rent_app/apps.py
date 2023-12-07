from django.apps import AppConfig


class RentAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent_app'
    def ready(self):
        import rental.signals
    
    
