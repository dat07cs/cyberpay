from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from CyberPay.wallet.forms import MyForm
from CyberPay.wallet.models import Transaction, Account


@login_required
def home(request):
    user = request.user
    latest_transactions = Transaction.objects.filter(account__user_id=user.id).order_by('-created')[:10]
    return render(request, 'wallet/base.html', {'transactions': latest_transactions})


@login_required
def transactions(request):
    user = request.user
    result = Transaction.objects.filter(account__user_id=user.id).order_by('-created')
    return render(request, 'wallet/transactions.html', {'transactions': result})


@login_required
def deposit(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            account = Account.objects.get(pk=request.user.id)
            transaction = Transaction.objects.create(account=account)
            transaction.created = datetime.now()
            transaction.balance_before = account.balance
            transaction.balance_after = account.balance + form.cleaned_data.get('amount')
            account.balance = transaction.balance_after
            account.save()
            transaction.save()
            return HttpResponseRedirect('transactions')
    else:
        form = MyForm()
    return render(request, 'wallet/transaction_form.html', {'form': form})


@login_required
def withdraw(request):
    return HttpResponseRedirect('transactions')
