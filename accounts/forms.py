from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


GLASS_STYLE = (
    'background: rgba(255, 255, 255, 0.03); '
    'border: 1px solid rgba(0, 229, 255, 0.2); '
    'transition: all 0.3s ease;'
)
GLASS_ATTRS = {'class': 'form-control form-glass text-white', 'style': GLASS_STYLE}


class CyberRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Required. Provide a valid neural address (email)."
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(GLASS_ATTRS)
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Enter node username'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Enter connection email'
            elif 'password' in field_name:
                field.widget.attrs['placeholder'] = '••••••••'


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Node username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Neural address (email)',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update(GLASS_ATTRS)
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This node username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This neural address is already registered.")
        return email


class CyberPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'old_password': 'Current passkey',
            'new_password1': 'New passkey',
            'new_password2': 'Confirm new passkey',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs.update(GLASS_ATTRS)
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '••••••••')
