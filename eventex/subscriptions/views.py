from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            send_email = EmailMessage(
                subject='Confirmação de Inscrição',
                body=body,
                from_email='contato@eventex.com.br',
                to=['contato@eventex.com.br',
                    form.cleaned_data['email']]
            )
            send_email.send()
            messages.success(request, 'Inscrição realizada com sucesso')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
    else:
        context = {'form': SubscriptionForm()}
        return render(request, 'subscriptions/subscription_form.html', context)
