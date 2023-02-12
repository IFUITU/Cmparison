from django.urls import path
from .views import compare, download, IndexView, service, about_view
app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("compare/", compare, name="compare"),
    path("done/", download, name="done"),
    path("service/<str:service_name>/", service, name='service'),
    path("about/", about_view, name="about"),
    
]