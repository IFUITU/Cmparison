from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import User
from .forms import UserForm

class UserView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('main:done')
    template_name = 'user_register.html'
