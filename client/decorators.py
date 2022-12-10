from django.shortcuts import redirect
from functools import wraps

def notloggedin_required(funct):
    @wraps(funct)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:compare")
        return funct(request, *args, **kwargs)
    return wrapper