from django.urls import path,include,re_path

from .views import *

from django.conf import settings
from .schema import schema_view
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'rental', RentalViewSet)
router.register(r'ihas', IhaViewSet)
router.register(r'contact', ContactViewSet)


app_name="api"
urlpatterns = [
    path('', include(router.urls)),
   
                            
    ## Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('rentals/create/',RentalListCreateView.as_view(),name="rental_create"),
    path('rental/dates/<int:id>/',IhaRentDaysAPIView.as_view(),name="ihas_rent_days"),
    path('rental/delete/<int:pk>/',RentalDeleteAPIView.as_view(),name="rental-delete"),
    path('rental/user/<int:id>/',RentalGetAPIView.as_view(),name="users_rent"),
    
    ## get User's rental
   

    path('iha/type/',IhaTypeCreateAPIView.as_view(),name="iha_create"),
 
   

    
]
 
   

    

