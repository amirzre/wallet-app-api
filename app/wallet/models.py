from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.db.models import Count, Sum, Q
from django.db.models.functions import Coalesce


class Transaction(models.Model):
    """User transactions"""
    CHARGE = 1
    PURCHASE = 2
    TRANSFER_RECEIVED = 3
    TRANSFER_SENT = 4

    TRANSACTION_TYPE_CHOICES = (
        (CHARGE, 'Charge'),
        (PURCHASE, 'Purchase'),
        (TRANSFER_RECEIVED, 'Transfer Received'),
        (TRANSFER_SENT, 'Transfer Sent'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='transactions',
        verbose_name=_('user')
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES,
        default=CHARGE,
        verbose_name=_('transaction type')
    )
    amount = models.BigIntegerField(verbose_name=_('amount'))
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time')
    )

    def __str__(self):
        return f'{self.get_transaction_type_display()}'

    @classmethod
    def get_report(cls):
        """Show all users and their balance"""
        positive_transactions = Sum(
            'transaction__amount',
            filter=Q(transactions__transaction_type__in=[1, 3])
        )
        negative_transactions = Sum(
            'transaction__amount',
            filter=Q(transactions__transaction_type_in=[2, 4])
        )
        users = get_user_model().objects.all().annotate(
            transactions_count=Count('transactions__id'),
            balance=Sum(Coalesce(positive_transactions, 0) -
                        Coalesce(negative_transactions, 0))
        )
        return users

    @classmethod
    def get_total_balance(cls):
        """Retrieve balance for all users"""
        queryset = cls.get_report()
        return queryset.aggregate(Sum('balance'))

    @classmethod
    def get_user_balance(cls, user):
        """Retrieve balance for current user"""
        positive_transactions = Sum(
            'amount',
            filter=Q(transaction_type__in=[1, 3])
        )
        negative_transactions = Sum(
            'amount',
            filter=Q(transaction_type__in=[2, 4])
        )
        user_balance = user.transactions.all().aggregate(
            balance=Coalesce(positive_transactions, 0) -
            Coalesce(negative_transactions, 0)
        )
        return user_balance.get('balance', 0)


class UserBalance(models.Model):
    """User balance model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='balance_records',
        verbose_name=_('user')
    )
    balance = models.BigIntegerField(verbose_name=_('balance'))
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time')
    )

    def __str__(self):
        return str(self.balance)

    @classmethod
    def record_user_balance(cls, user):
        """Record balance for current user"""
        balance = Transaction.get_user_balance(user)
        instance = cls.objects.create(user=user, balance=balance)
        return instance

    @classmethod
    def record_all_user_balance(cls):
        """Record balance for all users"""
        for user in get_user_model().objects.all():
            return cls.record_user_balance(user)


class TransferTransaction(models.Model):
    """Transfer transaction model"""
    sender_transaction = models.OneToOneField(
        Transaction,
        on_delete=models.RESTRICT,
        related_name='sent_transfers',
        verbose_name=_('sender transaction')
    )
    receiver_transaction = models.OneToOneField(
        Transaction,
        on_delete=models.RESTRICT,
        related_name='received_transfers',
        verbose_name=_('receiver transaction')
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time')
    )

    def __str__(self):
        return f'{self.sender_transaction} - {self.receiver_transaction}'

    @classmethod
    def transfer(cls, sender, receiver, amount):
        """Transfer amount between two users"""
        if Transaction.get_user_balance(sender) < amount:
            return 'Transaction not allowed, insufficient balance!'

        with transaction.atomic():
            sender_transaction = Transaction.objects.create(
                user=sender,
                amount=amount,
                transaction_type=Transaction.TRANSFER_SENT,
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver,
                amount=amount,
                transaction_type=Transaction.TRANSFER_RECEIVED,
            )

            instance = cls.objects.create(
                sender_transaction=sender_transaction,
                receiver_transaction=receiver_transaction
            )
        return instance
