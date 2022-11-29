from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy

from . import views


app_name = 'users'

urlpatterns = [
    path(
        'signup/done/', views.RegisterDoneView.as_view(), name='register_done'
    ),
    path('signup/', views.RegisterUserView.as_view(), name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path(
        'logout/',
        login_required(auth_views.LogoutView.as_view(
            template_name='users/logged_out.html'
        )),
        name='logout'
    ),
    path(
        'register/activate/<str:sign>/',
        views.user_activate,
        name='register_activate'
    ),
    path(
        'reset/<uidb64>/<token>/',
        login_required(auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("login"),
            template_name="users/password_reset_confirm.html"
        )),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/done/',
        login_required(auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        )),
        name='password_reset_done'
    ),
    path(
        'password_reset_form/',
        login_required(auth_views.PasswordResetView.as_view(
            template_name='users/password_reset_form.html'
        )),
        name='password_reset_form'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/password_change_form.html'
        ),
        name='password_change_form'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
