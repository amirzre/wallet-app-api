from rest_framework import serializers
from wallet.models import (
    Transaction, UserBalance, TransferTransaction
)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transaction object"""

    class Meta:
        model = Transaction
        fields = (
            'id', 'user', 'transaction_type', 'amount', 'created_time'
        )
        read_only_fields = ('id',)


class UserBalanceSerializer(serializers.ModelSerializer):
    """Serializer for user balance object"""

    class Meta:
        model = UserBalance
        fields = ('id', 'user', 'balance', 'created_time')
        read_only_fields = ('id',)


class TransferTransactionSerializer(serializers.ModelSerializer):
    """Serializer for transfer transaction object"""
    sender_transaction = TransactionSerializer(many=False)
    receiver_transaction = TransactionSerializer(many=False)

    class Meta:
        model = TransferTransaction
        fields = (
            'id', 'sender_transaction', 'receiver_transaction', 'created_time'
        )
        read_only_fields = ('id',)


class TransferTransactionDetailSerializer(TransferTransactionSerializer):
    """Serialize a transfer transaction"""
    sender_transaction = TransactionSerializer(many=False, read_only=True)
    receiver_transaction = TransactionSerializer(many=False, read_only=True)
