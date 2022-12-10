from django.urls import path
from .views import UserRegister, user_login, user_logout

app_name = 'client'

urlpatterns = [
    path('user-register/', UserRegister.as_view(), name="user-register"),
    path("user-login/", user_login, name="user-login"),
    path("user-logout/", user_logout, name="user-logout"),
]
