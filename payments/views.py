import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY

def buy_order(request, order_id):
    """Создает платеж для заказа"""
    order = get_object_or_404(Order, id=order_id)
    if not order.items.exists():
        return JsonResponse({"error": "Заказ пуст"}, status=400)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": order.items.first().currency,
                    "product_data": {
                        "name": f"Order {order.id}",
                    },
                    "unit_amount": int(order.total_amount * 100),  # Stripe требует сумму в центах
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
    )

    return JsonResponse({"session_id": session.id})



def item_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "payments/item.html", {"item": item, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY})

def home(request):
    items = Item.objects.all()  # Получаем все товары из базы данных
    return render(request, 'payments/home.html', {'items': items,
    'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})  # Передаем товары в шаблон


def create_order(request):
    """Создает заказ из списка товаров"""
    item_ids = request.GET.getlist("items")  # Получаем id товаров из запроса
    items = Item.objects.filter(id__in=item_ids)

    if not items.exists():
        return JsonResponse({"error": "Нет доступных товаров"}, status=400)

    order = Order.objects.create()
    order.items.set(items)
    order.calculate_total()

    return JsonResponse({"order_id": order.id, "total_amount": order.total_amount})


def buy_item(request, item_id):
    """Создаёт Stripe Session для оплаты товара"""
    item = get_object_or_404(Item, id=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",  # Или другая валюта из модели
                    "product_data": {"name": item.name},
                    "unit_amount": int(item.price * 100),  # Stripe требует цену в центах
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )

    return JsonResponse({"id": session.id})

def order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/order.html", {"order": order})
