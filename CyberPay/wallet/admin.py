from django.contrib import admin

from CyberPay.wallet.models import Account, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
