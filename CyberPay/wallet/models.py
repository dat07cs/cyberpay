from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    updated = models.DateTimeField(default=timezone.now)

    @receiver(post_save, sender=User)
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)

    def __str__(self):
        name = self.user.get_full_name()
        return name if name else self.user.username


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField()
    balance_before = models.DecimalField(decimal_places=6, max_digits=20)
    balance_after = models.DecimalField(decimal_places=6, max_digits=20)
    note = models.CharField(max_length=255, null=True)

    @property
    def amount(self):
        return self.balance_after - self.balance_before

    def __str__(self):
        return '{} at {:%Y-%m-%d %H:%M:%S %z} (before=${:,.2f}, after=${:,.2f})'\
            .format(self.account, self.created, self.balance_before, self.balance_after)
