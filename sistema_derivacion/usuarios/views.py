from django.shortcuts import render
from usuarios.models import Usuario
import hashlib

# Create your views here.
def checkStatus(request):
    pass

def login(request):

    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        hashed = hashlib.md5(password.encode('utf-8')).hexdigest()
        check = Usuario.objects.filter(correo = correo, contraseña = hashed)
        if check:
            request.session['estadoSesion'] = True
            request.session['correo'] = correo.upper()
            datos = {'correo' : correo}
            return render(request, 'menuA.html', datos)
        else:
            datos = {'r': 'Usuario no encontrado'}
            return render(request, 'login.html', datos)

def mostrarLogin (request):
    return render(request, 'login.html')
