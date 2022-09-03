from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from wallet import models


class TransactionSiteTests(TestCase):
    """Test transaction page in admin panel"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='testpass',
        )
        self.client.force_login(user=self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
        )
        self.transaction = models.Transaction.objects.create(
            user=self.user,
            transaction_type=1,
            amount=100,
        )
        self.user_balance = models.UserBalance.objects.create(
            user=self.user,
            balance=100,
        )
        self.sender_transaction = models.Transaction.objects.create(
            user=self.user,
            transaction_type=4,
            amount=100,
        )
        self.receiver_transaction = models.Transaction.objects.create(
            user=self.user,
            transaction_type=3,
            amount=100,
        )
        self.transfer_transaction = models.TransferTransaction.objects.create(
            sender_transaction=self.sender_transaction,
            receiver_transaction=self.receiver_transaction,
        )

    def test_transaction_listed(self):
        """Test that transaction are listed in transaction page"""
        url = reverse('admin:wallet_transaction_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.transaction.amount)
        self.assertEqual(res.status_code, 200)

    def test_transaction_change_page(self):
        """Test that the transaction edit page works"""
        url = reverse(
            'admin:wallet_transaction_change',
            args=[self.transaction.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_transaction_create_page(self):
        """Test that the transaction create page works"""
        url = reverse('admin:wallet_transaction_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_transaction_delete_page(self):
        """Test that the transaction delete page works"""
        url = reverse(
            'admin:wallet_transaction_delete',
            args=[self.transaction.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_balance_listed(self):
        """Test that user balance are listed in user balance page"""
        url = reverse('admin:wallet_userbalance_changelist')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user_balance.balance)

    def test_user_balance_change_page(self):
        """Test that the user balance edit page works"""
        url = reverse(
            'admin:wallet_userbalance_change',
            args=[self.user_balance.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_balance_create_page(self):
        """Test that the user balance create page works"""
        url = reverse('admin:wallet_userbalance_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_balance_delete_page(self):
        """Test that the user balance delete page works"""
        url = reverse(
            'admin:wallet_userbalance_delete',
            args=[self.user_balance.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_transfer_transaction_listed(self):
        """Test that transfer transaction are listed
        in transfer transaction page"""
        url = reverse(
            'admin:wallet_transfertransaction_changelist'
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(
            res, self.transfer_transaction.sender_transaction
        )
        self.assertContains(
            res, self.transfer_transaction.receiver_transaction
        )

    def test_transfer_transaction_change_page(self):
        """Test that the transfer transaction edit page works"""
        url = reverse(
            'admin:wallet_transfertransaction_change',
            args=[self.transfer_transaction.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_transfer_transaction_create_page(self):
        """Test that the transfer transaction create page works"""
        url = reverse('admin:wallet_transfertransaction_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_transfer_transaction_delete_page(self):
        """Test that the transfer transaction delete page works"""
        url = reverse(
            'admin:wallet_transfertransaction_delete',
            args=[self.transfer_transaction.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
