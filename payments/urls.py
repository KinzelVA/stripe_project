from django.urls import path
from .views import buy_order, item_view, home, create_order, buy_item


urlpatterns = [
    path("home/",home, name="home"),
    path("", home, name="root"),  # Главная страница
    path("create_order/", create_order, name="create_order"),
    path("buy_order/<int:order_id>/", buy_order, name="buy_order"),
    path("item/<int:item_id>/", item_view, name="item"),
    path("buy/<int:item_id>/", buy_item, name="buy"),
]
