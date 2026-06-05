from django import forms
from django.contrib.auth.models import User

from shop.models import Product, Review, Feedback


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'description',
            'price', 'old_price', 'image', 'image_upload', 'badge',
            'stock', 'in_stock', 'cpu', 'gpu', 'ram', 'storage',
            'mobo', 'psu', 'cooler', 'case', 'is_featured', 'is_trending',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'category': forms.Select(attrs={'class': 'form-select form-glass bg-dark border-secondary text-white'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white', 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white', 'step': '0.01'}),
            'image': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'image_upload': forms.FileInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'badge': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cpu': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'gpu': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'ram': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'storage': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'mobo': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'psu': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'cooler': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'case': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_trending': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'author_name', 'rating', 'title', 'content', 'is_approved', 'category', 'source']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select form-glass bg-dark border-secondary text-white'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white', 'min': 1, 'max': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white'}),
            'content': forms.Textarea(attrs={'class': 'form-control form-glass bg-transparent border-secondary text-white', 'rows': 4}),
            'is_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-select form-glass bg-dark border-secondary text-white'}),
            'source': forms.Select(attrs={'class': 'form-select form-glass bg-dark border-secondary text-white'}),
        }


class FeedbackStatusForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select form-glass bg-dark border-secondary text-white'}),
        }
