from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CyberRegisterForm, EditProfileForm, CyberPasswordChangeForm

class CyberLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Failed to establish connection. Invalid credentials.")
        return super().form_invalid(form)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"Connection established. Welcome back, {username}.")
        return super().form_valid(form)

class CyberRegisterView(CreateView):
    form_class = CyberRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shop:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Node initialized successfully! Enter credentials to connect.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to initialize node. Please check your parameters.")
        return super().form_invalid(form)

def logout_view(request):
    auth_logout(request)
    messages.info(request, "Connection terminated. Node disconnected.")
    return redirect('shop:home')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Node profile updated successfully.")
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, "Failed to update profile. Check the form below.")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CyberPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Passkey updated. Node security reinforced.")
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, "Failed to change passkey. Check the form below.")
    else:
        form = CyberPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})
