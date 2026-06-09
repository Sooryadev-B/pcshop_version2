from django import forms
from django.contrib.auth.models import User

from shop.models import Product, Review, Feedback, Deal, Category


GLASS_INPUT = 'form-control form-glass bg-transparent border-secondary text-white'
GLASS_SELECT = 'form-select form-glass bg-dark border-secondary text-white'
GLASS_TEXTAREA = 'form-control form-glass bg-transparent border-secondary text-white'
CHECKBOX = 'form-check-input'


class ProductForm(forms.ModelForm):
    deals = forms.ModelMultipleChoiceField(
        queryset=Deal.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Assign to Deals',
        help_text='Select active promotions this product appears in',
    )

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'description',
            'is_builder_part', 'component_type', 'wattage', 'socket',
            'price', 'old_price', 'image', 'image_upload', 'badge',
            'stock', 'in_stock', 'cpu', 'gpu', 'ram', 'storage',
            'mobo', 'psu', 'cooler', 'case', 'is_featured', 'is_trending',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'slug': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'category': forms.Select(attrs={'class': GLASS_SELECT}),
            'description': forms.Textarea(attrs={'class': GLASS_TEXTAREA, 'rows': 4}),
            'is_builder_part': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'component_type': forms.Select(attrs={'class': GLASS_SELECT}),
            'wattage': forms.NumberInput(attrs={'class': GLASS_INPUT, 'min': 0}),
            'socket': forms.TextInput(attrs={'class': GLASS_INPUT, 'placeholder': 'e.g. AM5, LGA1700'}),
            'price': forms.NumberInput(attrs={'class': GLASS_INPUT, 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': GLASS_INPUT, 'step': '0.01'}),
            'image': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'image_upload': forms.FileInput(attrs={'class': GLASS_INPUT}),
            'badge': forms.TextInput(attrs={'class': GLASS_INPUT, 'placeholder': 'FLAGSHIP, POPULAR, NEW'}),
            'stock': forms.NumberInput(attrs={'class': GLASS_INPUT}),
            'in_stock': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'cpu': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'gpu': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'ram': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'storage': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'mobo': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'psu': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'cooler': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'case': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'is_featured': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'is_trending': forms.CheckboxInput(attrs={'class': CHECKBOX}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')
        self.fields['deals'].queryset = Deal.objects.all().order_by('-starts_at')
        if self.instance.pk:
            self.fields['deals'].initial = self.instance.deals.all()

    def save(self, commit=True):
        product = super().save(commit=commit)
        if commit:
            selected_deals = self.cleaned_data.get('deals', [])
            for deal in Deal.objects.filter(products=product):
                if deal not in selected_deals:
                    deal.products.remove(product)
            for deal in selected_deals:
                deal.products.add(product)
        return product


class DealForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(in_stock=True).order_by('name'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Products in this Deal',
    )

    class Meta:
        model = Deal
        fields = [
            'title', 'slug', 'description', 'discount_label', 'badge',
            'starts_at', 'ends_at', 'is_active', 'products',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'slug': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'description': forms.Textarea(attrs={'class': GLASS_TEXTAREA, 'rows': 3}),
            'discount_label': forms.TextInput(attrs={'class': GLASS_INPUT, 'placeholder': 'e.g. 15% OFF'}),
            'badge': forms.TextInput(attrs={'class': GLASS_INPUT, 'placeholder': 'e.g. FLASH SALE'}),
            'starts_at': forms.DateTimeInput(attrs={'class': GLASS_INPUT, 'type': 'datetime-local'}),
            'ends_at': forms.DateTimeInput(attrs={'class': GLASS_INPUT, 'type': 'datetime-local'}),
            'is_active': forms.CheckboxInput(attrs={'class': CHECKBOX}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['products'].initial = self.instance.products.all()
            for field_name in ('starts_at', 'ends_at'):
                value = getattr(self.instance, field_name)
                if value:
                    self.initial[field_name] = value.strftime('%Y-%m-%dT%H:%M')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'id_key']
        widgets = {
            'name': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'id_key': forms.TextInput(attrs={'class': GLASS_INPUT, 'placeholder': 'e.g. gpu, cpu, prebuilt'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'email': forms.EmailInput(attrs={'class': GLASS_INPUT}),
            'first_name': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'last_name': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'is_active': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'is_staff': forms.CheckboxInput(attrs={'class': CHECKBOX}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'author_name', 'rating', 'title', 'content', 'is_approved', 'category', 'source']
        widgets = {
            'product': forms.Select(attrs={'class': GLASS_SELECT}),
            'author_name': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'rating': forms.NumberInput(attrs={'class': GLASS_INPUT, 'min': 1, 'max': 5}),
            'title': forms.TextInput(attrs={'class': GLASS_INPUT}),
            'content': forms.Textarea(attrs={'class': GLASS_TEXTAREA, 'rows': 4}),
            'is_approved': forms.CheckboxInput(attrs={'class': CHECKBOX}),
            'category': forms.Select(attrs={'class': GLASS_SELECT}),
            'source': forms.Select(attrs={'class': GLASS_SELECT}),
        }


class FeedbackStatusForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': GLASS_SELECT}),
        }
