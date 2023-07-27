from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.log_out_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('change_password/', views.ChangePasswordView.as_view(template_name='account/password-change-form.html'), name='change-password'),
    path('change_profile/', views.change_profile, name='change-profile'),
    path(
        'password_reset/', 
        PasswordResetView.as_view(
            template_name='account/password_reset_form.html',
            email_template_name='account/password_reset_email.html',
            success_url=reverse_lazy("account:password_reset_done"),
        ), 
        name='password_reset'
    ),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html',
            post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
            success_url = reverse_lazy("account:password_reset_complete"),
        ), 
        name='password_reset_confirm'
    ),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/my_properties/', views.my_properties, name='my-properties'),
    path('dashboard/my_wish_list/', views.my_wish_list, name='wish-list'),
]