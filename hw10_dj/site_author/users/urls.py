from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView


from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(template_name='users/login.html', form_class=LoginForm,
                                      redirect_authenticated_user=True), name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
