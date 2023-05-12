import requests
from django.shortcuts import render, redirect

from authapp.models import Register
from authapp.views import check_if_someone_logged
from exchange_rate.forms import CurrencyForm
from exchange_rate.models import ExchangeRateHistory


def exchange_rate(request):
    try:
        user = Register.objects.get(id=request.session.get('user_id'))
        is_logged = check_if_someone_logged(request)
    except:  # NOQA
        return redirect('home')

    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            currency_code = form.cleaned_data['base_currency']

            response = requests.get(
                f'https://v6.exchangerate-api.com/v6/0375590855b556765b4eafb5/latest/{currency_code}')

            chosen_to_exchange = form.cleaned_data['target_currency']
            data = response.json()
            rate = data['conversion_rates'][chosen_to_exchange]

            exchange_history = ExchangeRateHistory(
                user=user,
                base_currency=currency_code,
                target_currency=chosen_to_exchange,
                rate=rate
            )

            exchange_history.save()

            history = ExchangeRateHistory.objects.filter(user=user).order_by('-timestamp')

            context = {
                'currency_code': currency_code,
                'rate': rate,
                'rate-currency': data['conversion_rates'],
                'chosen_to_exchange': chosen_to_exchange,
                'form': form,
                'is_logged': is_logged,
                'user': user,
                'history': history
            }
            return redirect('exchange_rate')
            # return redirect(request, 'exchange_rate.html', context)
    else:
        form = CurrencyForm()

        history = ExchangeRateHistory.objects.filter(user=user).order_by('-timestamp')

        context = {
            'is_logged': is_logged,
            'user': user,
            'form': form,
            'history': history,
        }
        return render(request, 'exchange_rate.html', context)


def exchange_delete(request, exchange_id):
    exchange = ExchangeRateHistory.objects.get(id=exchange_id)
    exchange.delete()
    return redirect('exchange_rate')
