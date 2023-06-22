from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.log_out_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('change_password/', views.ChangePasswordView.as_view(template_name='account/password-change-form.html'), name='change-password'),
    path('change_profile/', views.change_profile, name='change-profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/my_properties/', views.my_properties, name='my-properties'),
    path('dashboard/my_wish_list/', views.my_wish_list, name='wish-list'),
]