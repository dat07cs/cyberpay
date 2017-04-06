import sys

from django import forms


class MyForm(forms.Form):
    amount = forms.DecimalField(min_value=sys.float_info.min, max_value=10 ** 12)
