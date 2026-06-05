from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CyberLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.CyberRegisterView.as_view(), name='register'),
]
