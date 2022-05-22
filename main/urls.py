from django.urls import path
from .views import compare, download
app_name = "main"
urlpatterns = [
    path("", compare, name="compare"),
    path("done/", download, name="done")
]