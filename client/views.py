from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .permissions import notLoginRequiredMixin
from .models import User
from .forms import UserForm, LoginForm
from .decorators import notloggedin_required

class UserRegister(notLoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('main:done')
    template_name = 'user_register.html'
    login_url = 'main:compare' #if user is logged in redirect to login_url
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] != data['confirm']:
                ValidationError("Password confirmation is not valid!")
            del data['confirm']
            user = User(**data)
            
            user.set_password(user.password)
            user.save()
            return redirect("client:user-login")
        return super().post(request)


@notloggedin_required
def user_login(request):
    # request.title = 'Login'
    form = LoginForm()
    if request.POST:
        form  = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main:index')
            
            form.add_error('username', 'Username or Password is not valid')
    return render(request, 'login.html', {'form':form})


@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("client:user-login")
    # return redirect("client:user-login")