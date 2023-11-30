from multiprocessing import Process
from os import kill
from signal import SIGTERM, SIGINT


from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .compare import make_comparison
from .forms import ComparisonForm 
from .models import Service


class IndexView(LoginRequiredMixin, ListView):
    model = Service
    template_name = "pages/index.html"


@login_required
def service(request, service_name):
    if service_name == 'Compare':
        return redirect('main:compare')
    return redirect("main:index")

@login_required
def about_view(request):
    return render(request, 'pages/about.html')
from django.http import JsonResponse

@login_required
def compare(request):

    if request.method == "POST":
        data = ComparisonForm(data=request.POST, files=request.FILES)
        if data.is_valid():

            start = datetime.now()
            try:
                make_comparison(data, request)
            except Exception as ex:
                return redirect("main:compare")

            # compare_thread = Process(target=make_comparison, args=(data, request), daemon=True)
            # compare_thread.start()
            # kill(compare_thread.pid, SIGKILL)
            # compare_thread.join()
            # return redirect("main:loading", pid=compare_thread.pid)
            print(datetime.now() - start,)
            # return JsonResponse({"PID":compare_thread.pid})
            return redirect("main:done")

    context = {}
    context['form'] = ComparisonForm()
    return render(request, "pages/compare.html", context)


@login_required
def download(request):
    context = {}
    context['COMPARISON_FILE'] = f'/media/sample_{request.user}.xlsx'
    return render( request, "pages/result.html", context)

