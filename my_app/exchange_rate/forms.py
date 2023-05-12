from django import forms


class CurrencyForm(forms.Form):
    base_choices = [
        ('BGN', 'BGN'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('TRY', 'TRY'),
    ]

    target_choices = [
        ('USD', 'USD'),
        ('BGN', 'BGN'),
        ('EUR', 'EUR'),
        ('GBP', 'GBP'),
        ('TRY', 'TRY'),
    ]

    base_currency = forms.ChoiceField(label='Base Currency', choices=base_choices)
    target_currency = forms.ChoiceField(label='Target Currency', choices=target_choices)
