from django.urls import path
from .views import compare, index

urlpatterns = [
    path("", compare, name="compare")
]