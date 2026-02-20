from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/',register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    path('products/', product_list, name='products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('checkout/',checkout, name='checkout'),
    path('category/<int:category_id>/',category_products, name='category_products'),
]
