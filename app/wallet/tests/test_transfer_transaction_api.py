from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wallet.models import Transaction


TRANSFER_TRANSACTION_URL = reverse(
    'wallet:transfer-list'
)


class PublicUserBalanceApiTests(TestCase):
    """Test the publicly available transfer transaction API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving
        transfer transaction"""
        res = self.client.get(TRANSFER_TRANSACTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserBalanceApiTests(TestCase):
    """Test the authorized user transfer transaction API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
        )
        self.user2 = get_user_model().objects.create_user(
            email='other@email.com',
            password='testpass',
        )
        self.sender_transaction = Transaction.objects.create(
            user=self.user,
            transaction_type=4,
            amount=100,
        )
        self.receiver_transaction = Transaction.objects.create(
            user=self.user2,
            transaction_type=3,
            amount=100,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_transfer_transaction_successful(self):
        """Test creating a new transfer transaction"""
        payload = {
            "sender_transaction": {
                "user": self.user.id,
                "transaction_type": 4,
                "amount": 10
            },
            "receiver_transaction": {
                "user": self.user2.id,
                "transaction_type": 3,
                "amount": 10
            }
        }
        res = self.client.post(
            TRANSFER_TRANSACTION_URL, payload, format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_transfer_transaction_invalid(self):
        """Test creating a new user balance with invalid payload"""
        payload = {
            'sender_transaction': self.sender_transaction,
            'receiver_transaction': '',
        }
        res = self.client.post(TRANSFER_TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
