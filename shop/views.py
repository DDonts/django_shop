import stripe

from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import Item, Order


def index(request):
    items = Item.objects.all()
    if not request.session.session_key:
        request.session.save()

    order = Order.objects.get_or_create(session_id=request.session.session_key)[0]
    context = {'items': items, 'order': order}
    return render(request, 'index.html', context)


def item_view(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'item': item}
    return render(request, 'item.html', context)


def add_to_order(request, item_id):
    item = Item.objects.get(id=item_id)
    order = Order.objects.get_or_create(session_id=request.session.session_key)[0]
    order.items.add(item)
    order.save()
    return redirect(index)


def success_view(request):
    order = Order.objects.get_or_create(session_id=request.session.session_key)[0]
    order.delete()
    return render(request, 'success.html')


def cancelled_view(request):
    return render(request, 'cancelled.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def get_items_from_order(request):
    order = Order.objects.get(session_id=request.session.session_key)
    items = order.items.all()
    stripe_item_list = []
    for item in items:
        tmp = {'name': item.name, 'quantity': 1, 'currency': 'usd', 'amount': int(item.price * 100)}
        stripe_item_list.append(tmp)
    return stripe_item_list


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        items = get_items_from_order(request)
        try:
            checkout_session = stripe.checkout.Session.create(
                stripe_version="2020-08-27",
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=f'{domain_url}cancelled/',
                payment_method_types=['card'], mode='payment',
                line_items=items)

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
