from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, UserProfileForm, UserAuthenticationForm
from .models import User
from property.models import PropertyWishList, Property


class CustomLoginView(LoginView):
    form_class = UserAuthenticationForm
    template_name = "account/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(259200)
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


def log_out_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have logged out.')
        return redirect('account:login')
    

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def dashboard(request):
    user = get_object_or_404(User, id=request.user.id)
    profile_form = UserProfileForm(instance=user)
    password_form = PasswordChangeForm(user=user)
    context = {'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'account/dashboard.html', context)


@login_required
def change_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
    else:
        form = UserProfileForm(instance=user)
    context ={'form': form}
    return render(request, 'account/profile-change-form.html', context)


class ChangePasswordView(PasswordChangeView, LoginRequiredMixin):
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return redirect('account:dashboard')


@login_required
def my_wish_list(request):
    wish_list = PropertyWishList.objects.filter(user_id=request.user.id)
    context = {'wish_list': wish_list}
    return render(request, 'account/partials/wish-list.html', context)


@login_required
def my_properties(request):
    qs = Property.objects.filter(owner_id=request.user.id)
    return render(request, 'account/partials/my-properties.html', {'qs': qs})