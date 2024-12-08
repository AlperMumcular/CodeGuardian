from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .main import main

# Create your views here.
def index(request):
    return render(request, 'url/index.html')

@csrf_exempt
def generate_report(request, path):
    if request.method == 'POST':
        ##Some function here##
        # TODO 
        main()
        
        return HttpResponse(f"Report generated for: {path}", status=200)

    return HttpResponse("Invalid Request", status=400)