from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),

    path('category/<int:category_id>/', views.get_category_detail, name="category"),

    path('products/', views.ShopView.as_view(), name="products"),
    path('product_detail/<int:product_id>/', views.get_product_details, name="product_detail"),
    path('product/<int:product_id>/add/', views.add_remove_product_quantity, {'op_type': 'add'}, name="add_product"),
    path('product/<int:product_id>/remove/', views.add_remove_product_quantity, {'op_type': 'remove'},
         name="remove_product"),

    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name="add_to_cart"),
    path('user/product-cart/', views.get_user_cart, name="user_cart"),

    path('user/cart/product/<int:ordered_item_id>/increase/', views.increase_product_quantity_in_cart,
         name="increase_product_in_cart"),
    path('user/cart/product/<int:ordered_item_id>/decrease/', views.decrease_product_quantity_in_cart,
         name="decrease_product_in_cart"),
    path('user/cart/product/<int:ordered_item_id>/remove/', views.remove_item_from_cart,
         name="remove_product_from_cart"),

    path('user/cart/checkout/', views.checkout, name="checkout"),
    path('user/cart/payment/', views.PaymentView.as_view(), name="payment"),

    path('contact-us/', views.ContactView.as_view(), name="contact_us"),
    path('about-us/', views.AboutView.as_view(), name="about_us"),
]
