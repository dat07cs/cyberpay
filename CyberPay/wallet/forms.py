from django import forms


class MyForm(forms.Form):
    amount = forms.DecimalField(min_value=0.01, max_value=10 ** 12, decimal_places=2)
    note = forms.CharField(max_length=255, required=False)
