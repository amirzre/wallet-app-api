from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet import views


router = DefaultRouter()

app_name = 'wallet'

urlpatterns = [
    path('', include(router.urls)),
]
