from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet import views


router = DefaultRouter()
router.register('transactions',
                views.TransactionViewSet,
                basename='transactions')
router.register('userbalance',
                views.UserBalanceViewSet,
                basename='userbalance')

app_name = 'wallet'

urlpatterns = [
    path('', include(router.urls)),
]
