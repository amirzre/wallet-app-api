from django.test import TestCase
from django.contrib.auth import get_user_model
from wallet import models


class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
        )

    def test_transaction_str(self):
        """Test the transaction string representation"""
        transaction = models.Transaction.objects.create(
            user=self.user,
            transaction_type=1,
            amount=100,
        )

        self.assertEqual(
            str(transaction),
            transaction.get_transaction_type_display()
        )

    def test_user_balance_str(self):
        """Test the user balance string representation"""
        user_balance = models.UserBalance.objects.create(
            user=self.user,
            balance=100,
        )

        self.assertEqual(str(user_balance), str(user_balance.balance))

    def test_transfer_transaction_str(self):
        """Test the transfer transaction string representation"""
        user2 = get_user_model().objects.create(
            email='other@email.com',
            password='testpass',
        )
        sender_transaction = models.Transaction.objects.create(
            user=self.user,
            transaction_type=4,
            amount=100,
        )
        receiver_transaction = models.Transaction.objects.create(
            user=user2,
            transaction_type=3,
            amount=100,
        )
        transfer_transaction = models.TransferTransaction.objects.create(
            sender_transaction=sender_transaction,
            receiver_transaction=receiver_transaction,
        )

        self.assertEqual(
            str(transfer_transaction),
            f'{transfer_transaction.sender_transaction} - {transfer_transaction.receiver_transaction}'
        )
