from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('deals/', views.deals, name='deals'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('builder/', views.builder, name='builder'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/', views.feedback, name='feedback'),
]
