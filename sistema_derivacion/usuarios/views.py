from django.shortcuts import render

# Create your views here.
def iniciarSesion(request):
    return render(request, 'login.html')