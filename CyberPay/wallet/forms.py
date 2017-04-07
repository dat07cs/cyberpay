from django import forms

from CyberPay.wallet.models import Account


class MyForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, max_value=10 ** 12, decimal_places=2)
    note = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.deposit = kwargs.pop('deposit', True)
        super(MyForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        data = self.cleaned_data['amount']
        account = Account.objects.filter(user_id=self.user.id).first()
        if not self.deposit and data > account.balance:
            raise forms.ValidationError(
                "Cannot withdraw more than the current balance of ${:,.2f}".format(account.balance))
        return data
