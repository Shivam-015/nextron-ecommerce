from django.urls import path
from . import views
urlpatterns = [
    path('' , views.home , name="home"),
    path('products/' , views.all_products , name="all_products"),
    path('contact/' , views.contact , name="contact"),
    path('profile/' , views.profile , name="profile"),
    path('product_details/<int:product_id>', views.product_details , name="product_details"),
    path('cart/' , views.cart , name="cart"),
    path('delete_from_cart/<int:item_id>',views.delete_from_cart,name='delete_from_cart'),
    path('add_to_cart/<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('increase<int:item_id>/' , views.increase , name="increase"),
    path('decrease<int:item_id>/' , views.decrease , name="decrease"),
] 

