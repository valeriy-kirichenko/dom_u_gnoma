from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

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
    
]
