from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wallet.models import Transaction
from wallet.serializers import TransactionSerializer


TRANSACTION_URL = reverse('wallet:transactions-list')


class PublicTransactionApiTests(TestCase):
    """Test the publicly available transaction API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving transactions"""
        res = self.client.get(TRANSACTION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTransactionApiTests(TestCase):
    """Test the authorized user transaction API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_transactions(self):
        """Test retrieving transactions"""
        Transaction.objects.create(
            user=self.user,
            transaction_type=1,
            amount=100
        )
        Transaction.objects.create(
            user=self.user,
            transaction_type=2,
            amount=10
        )
        res = self.client.get(TRANSACTION_URL)
        transactions = Transaction.objects.all().order_by('-created_time')
        serializer = TransactionSerializer(transactions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_transaction_limited_to_user(self):
        """Test that transactions returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='other@email.com',
            password='testpass',
        )
        Transaction.objects.create(
            user=user2,
            transaction_type=2,
            amount=10
        )
        transaction = Transaction.objects.create(
            user=self.user,
            transaction_type=1,
            amount=100
        )
        res = self.client.get(TRANSACTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['amount'], transaction.amount)

    def test_create_transaction_successful(self):
        """Test creating a new transaction"""
        payload = {
            'user': self.user.id,
            'transaction_type': 2,
            'amount': 20,
        }
        res = self.client.post(TRANSACTION_URL, payload)
        exists = Transaction.objects.filter(
            user=self.user,
            transaction_type=payload['transaction_type'],
            amount=payload['amount'],
        ).exists()

        self.assertTrue(exists)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_invalid(self):
        """Test creating a new transaction with invalid payload"""
        payload = {
            'user': self.user,
            'transaction_type': 1,
            'amount': '',
        }
        res = self.client.post(TRANSACTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
