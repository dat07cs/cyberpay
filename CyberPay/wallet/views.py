from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from CyberPay.wallet.forms import MyForm
from CyberPay.wallet.models import Transaction, Account


@login_required
def home(request):
    user = request.user
    latest_transactions = Transaction.objects.filter(account__user_id=user.id).order_by('-created')[:5]
    return render(request, 'wallet/base.html', {'transactions': latest_transactions})


@login_required
def transactions(request):
    user = request.user
    transaction_list = Transaction.objects.filter(account__user_id=user.id).order_by('-created')
    paginator = Paginator(transaction_list, 10)

    page = request.GET.get('page')
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return render(request, 'wallet/transactions.html', {'transactions': result})


@login_required
def deposit(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                create_transaction(Account.objects.select_for_update().get(user_id=request.user.id),
                                   form.cleaned_data['amount'],
                                   form.cleaned_data['note'])
            return HttpResponseRedirect(reverse('wallet:transactions'))
    else:
        form = MyForm()
    return render(request, 'wallet/deposit_form.html', {'form': form})


@login_required
def withdraw(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            with transaction.atomic():
                account = Account.objects.select_for_update().get(user_id=request.user.id)
                if amount <= account.balance:
                    create_transaction(account, amount * -1, form.cleaned_data['note'])
                    return HttpResponseRedirect(reverse('wallet:transactions'))
                else:
                    form.add_error('amount',
                                   "Cannot withdraw more than the current balance of ${:,.2f}".format(account.balance))
    else:
        form = MyForm()
    return render(request, 'wallet/withdraw_form.html', {'form': form})


def create_transaction(account, amount, note):
    old_balance = account.balance
    account.balance = old_balance + amount
    now = timezone.now()
    account.updated = now
    account.save()
    return Transaction.objects.create(account=account, created=now, balance_before=old_balance,
                                      balance_after=account.balance, note=note)
