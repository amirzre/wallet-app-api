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
router.register('transfer',
                views.TransferTransactionViewSet,
                basename='transfer-transaction')


app_name = 'wallet'

urlpatterns = [
    path('', include(router.urls)),
]
