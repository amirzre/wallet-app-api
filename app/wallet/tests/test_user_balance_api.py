from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from wallet.models import UserBalance
from wallet.serializers import UserBalanceSerializer


USER_BALANCE_URL = reverse('wallet:userbalance-list')


class PublicUserBalanceApiTests(TestCase):
    """Test the publicly available user balance API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retriving user balance"""
        res = self.client.get(USER_BALANCE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserBalanceApiTests(TestCase):
    """Test the authorized user, user balance API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_balance(self):
        """Test retrieving user balance"""
        UserBalance.objects.create(
            user=self.user,
            balance=100,
        )
        UserBalance.objects.create(
            user=self.user,
            balance=200,
        )
        res = self.client.get(USER_BALANCE_URL)
        user_balance = UserBalance.objects.all().order_by('-created_time')
        serializer = UserBalanceSerializer(user_balance, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_balance_limited_to_user(self):
        """Test that user balance returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email='other@email.com',
            password='testpass',
        )
        user_balance = UserBalance.objects.create(
            user=self.user,
            balance=100,
        )
        UserBalance.objects.create(
            user=user2,
            balance=200,
        )
        res = self.client.get(USER_BALANCE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['balance'], user_balance.balance)

    def test_create_user_balance_successful(self):
        """Test creating a new user balance"""
        payload = {
            'user': self.user.id,
            'balance': 100,
        }
        res = self.client.post(USER_BALANCE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_balance_invalid(self):
        """Test creating a new user balance with invalid payload"""
        payload = {'user': self.user, 'balance': ''}
        res = self.client.post(USER_BALANCE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
