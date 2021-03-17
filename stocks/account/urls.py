from django.urls import path
from . import views
from  django.contrib.auth import views as auth_views
from .forms import LoginForm, PwdResetForm

app_name = 'account'


urlpatterns = [
    path('register/', views.account_register, name="register"),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html', form_class=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login'), name='logout'),
    path('profile/edit/', views.edit_details, name='edit_details'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/user/password_reset_form.html',
                                                                success_url='password_reset_email_confirm',
                                                                email_template_name='account/user/password_reset_email.html',
                                                                form_class=PwdResetForm), name='pwdreset'),
]
