from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'code_sharing/home.html')

def mycodes(request):
    return HttpResponse('<h1>Explore your codes</h1>')

 