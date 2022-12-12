from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from fuzzywuzzy import fuzz
from django.views.decorators.http import require_http_methods

from .compare import make_comparison
from .forms import ComparisonForm 
from .models import Service

class IndexView(ListView):
    model = Service
    template_name = "pages/index.html"

def service(request, service_name):
    if service_name == 'Compare':
        return redirect('main:compare')
    return redirect("main:index")

def compare(request):
    if request.method == "POST":
        data = ComparisonForm(data=request.POST, files=request.FILES)
        if data.is_valid():
            start = datetime.now()
            make_comparison(data)
            print(datetime.now() - start)

            context = {}
            context['FIRST_FILE_NAME'] = data.cleaned_data['first_file']
            context['SECOND_FILE_NAME'] = data.cleaned_data['second_file']
            context['COMPARISON_FILE'] = '/media/sample.xlsx'
            return redirect("main:done")

    context = {}
    context['form'] = ComparisonForm()
    return render(request, "pages/compare.html", context)

def download(request):
    context = {}
    context['COMPARISON_FILE'] = '/media/sample.xlsx'
    return render( request, "pages/result.html", context)