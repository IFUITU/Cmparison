from django.http import HttpResponse
from django.shortcuts import redirect, render
from openpyxl import Workbook, load_workbook
from config.settings import MEDIA_ROOT, MEDIA_URL
# from transliterate import to_cyrillic, to_latin
from fuzzywuzzy import fuzz
from .forms import ComparisonForm
from django.views.decorators.http import require_http_methods
from .comparison_lab import make_comparison
from datetime import datetime

@require_http_methods(["GET"])
def index(request):
    context = {}
    context['form'] = ComparisonForm()
    
    return render(request, "pages/index.html", context)



def compare(request):
    if request.method == "POST":
        data = ComparisonForm(data=request.POST, files=request.FILES)
        if data.is_valid():
            start = datetime.now()
            make_comparison(data)
            print(datetime.now() - start)

            context = {}
            context['FIRST_FILE_NAME'] = data.cleaned_data['file_1']
            context['SECOND_FILE_NAME'] = data.cleaned_data['file_2']
            context['COMPARISON_FILE'] = '/media/sample.xlsx'

            return render( request, "pages/result.html", context)

    context = {}
    context['form'] = ComparisonForm()
    return render(request, "pages/index.html", context)