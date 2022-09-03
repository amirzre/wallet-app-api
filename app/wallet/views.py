from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from wallet.models import (
    Transaction, UserBalance, TransferTransaction
)
from wallet.serializers import (
    TransactionSerializer,
    UserBalanceSerializer,
    TransferTransactionSerializer,
    TransferTransactionDetailSerializer,
)


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """Base view set to manage database models"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-created_time')

    def perform_create(self, serializer):
        """Creating a new transaction"""
        serializer.save(user=self.request.user)


class TransactionViewSet(BaseViewSet):
    """Manage transaction in the database"""
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def get_user_balance(self, request, pk=None):
        """Retrieve balance for current user"""
        user = request.user
        balance = Transaction.get_user_balance(user)
        return Response({'user balance': balance})
