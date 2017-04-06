from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from CyberPay.wallet.models import User, Transaction


@login_required
def home(request):
    user = request.user
    latest_transactions = Transaction.objects.filter(account__user_id=user.id).order_by('-created')[:10]
    return render(request, 'wallet/transactions.html', {'transactions': latest_transactions})


@login_required
def transactions(request):
    user = User.objects.get(pk=request.user.id)
    return HttpResponse("All transactions of %s" % user)
