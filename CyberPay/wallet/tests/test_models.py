from django.contrib.auth.models import User
from django.test import TestCase

from CyberPay.wallet.models import Account, Transaction


class TestAccount(TestCase):
    def test_create_user(self):
        user = User.objects.create_user('user', 'user@test.com', 'Password@')
        self.assertIsNotNone(user)
        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertIsNotNone(account)
        self.assertEqual(account.balance, 0)
        self.assertEqual(str(account), 'user')


class TestTransaction(TestCase):
    def test_create_transaction(self):
        User.objects.create_user('user', 'user@test.com', 'Password@')
        account = Account.objects.first()
        amount = 1000000
        transaction = Transaction.objects.create(account=account, balance_before=0, balance_after=amount)
        self.assertEqual(transaction.amount, amount)
        self.assertTrue('before=$0.00, after=$1,000,000.00' in str(transaction))
