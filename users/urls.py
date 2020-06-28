from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name="sign_up"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
