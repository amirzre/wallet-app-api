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


class UserBalanceViewSet(BaseViewSet):
    """Manage user balance in database"""
    serializer_class = UserBalanceSerializer
    queryset = UserBalance.objects.all()


class TransferTransactionViewSet(viewsets.ModelViewSet):
    """Manage transfer transaction in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransferTransactionSerializer
    queryset = TransferTransaction.objects.all()

    def get_queryset(self):
        """Retrieve the transfer transaction for the authenticated user"""
        return self.queryset.select_related(
            'sender_transaction__user'
        )

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return TransferTransactionDetailSerializer
        return self.serializer_class


    def create(self, request, *args, **kwargs):
        serializer = TransferTransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            TransferTransaction.transfer(
                sender=serializer.validated_data.get(
                    'sender_transaction'
                )['user'],
                receiver=serializer.validated_data.get(
                    'receiver_transaction'
                )['user'],
                amount=serializer.validated_data['sender_transaction']['amount']
            )
            UserBalance.record_user_balance(
                user=self.request.user
            )
            return Response(
                data={'success': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
