from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CyberLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.CyberRegisterView.as_view(), name='register'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
]
