from django.urls import path
from .views import UserView

app_name = 'client'

urlpatterns = [
    path('', UserView.as_view(), name="user-view")
]
