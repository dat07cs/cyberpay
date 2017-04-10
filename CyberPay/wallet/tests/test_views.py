from django.contrib.auth.models import User
from django.test import TestCase

from CyberPay.wallet.models import Transaction, Account

BALANCE_STEP = 10000

NUM_TRANSACTIONS = 20

INITIAL_BALANCE = BALANCE_STEP * NUM_TRANSACTIONS


class SetupClass(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'Password@')
        account = self.user.account
        balance = account.balance
        for i in range(0, NUM_TRANSACTIONS):
            balance_before = balance
            balance += BALANCE_STEP
            Transaction.objects.create(account=account, balance_before=balance_before, balance_after=balance)
        account.balance = balance
        account.save()

        self.client.force_login(self.user)


class TestViews(SetupClass):
    def test_home(self):
        response = self.client.get('/wallet/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['transactions'].count(), 5)
        self.assertTemplateUsed(response, 'wallet/base.html')

    def test_transactions(self):
        response = self.client.get('/wallet/transactions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['transactions'].paginator.count, NUM_TRANSACTIONS)
        self.assertTemplateUsed(response, 'wallet/transactions.html')

    def test_deposit(self):
        response = self.client.get('/wallet/deposit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/deposit_form.html')
        amount = 50000
        note = 'deposit 50k'
        response = self.client.post('/wallet/deposit/', {'amount': amount, 'note': note})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/wallet/transactions/')
        self.assertEqual(Account.objects.first().balance, INITIAL_BALANCE + amount)
        self.assertEqual(Transaction.objects.count(), NUM_TRANSACTIONS + 1)
        transaction = Transaction.objects.order_by('-created').first()
        self.assertEqual(transaction.account.user_id, self.user.id)
        self.assertEqual(transaction.balance_before, INITIAL_BALANCE)
        self.assertEqual(transaction.balance_after, INITIAL_BALANCE + amount)
        self.assertEqual(transaction.note, note)

    def test_withdraw_success(self):
        response = self.client.get('/wallet/withdraw/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/withdraw_form.html')
        amount = 50000
        note = 'withdraw 50k'
        response = self.client.post('/wallet/withdraw/', {'amount': amount, 'note': note})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/wallet/transactions/')
        self.assertEqual(Account.objects.first().balance, INITIAL_BALANCE - amount)
        self.assertEqual(Transaction.objects.count(), NUM_TRANSACTIONS + 1)
        transaction = Transaction.objects.order_by('-created').first()
        self.assertEqual(transaction.account.user_id, self.user.id)
        self.assertEqual(transaction.balance_before, INITIAL_BALANCE)
        self.assertEqual(transaction.balance_after, INITIAL_BALANCE - amount)
        self.assertEqual(transaction.note, note)

    def test_withdraw_failed(self):
        response = self.client.get('/wallet/withdraw/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/withdraw_form.html')
        amount = INITIAL_BALANCE + 1000
        note = 'should fail'
        response = self.client.post('/wallet/withdraw/', {'amount': amount, 'note': note})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wallet/withdraw_form.html')
        self.assertEqual(Transaction.objects.count(), NUM_TRANSACTIONS)
        self.assertEqual(Account.objects.first().balance, INITIAL_BALANCE)
