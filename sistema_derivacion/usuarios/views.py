from django.shortcuts import render
from usuarios.models import Usuario
import hashlib

# Create your views here.
def mostrarLogin (request):
    datos = { 'img1' : 'logo_rancagua.png' }
    return render(request, 'login.html', datos)

def login(request):

    if request.method == 'POST':
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        hashed = hashlib.md5(contraseña.encode('utf-8')).hexdigest()
        usuario = Usuario.objects.filter(correo = correo, contraseña = hashed).first()

        if usuario:
            request.session['estadoSesion'] = True
            request.session['correo'] = usuario.correo
            request.session['rol'] = usuario.rol

            datos = {'correo' : usuario.correo, 'rol': usuario.rol.lower()}

            if usuario.rol == 'TENS':
                return render(request, 'menuT.html', datos)
            elif usuario.rol == 'AMBULANCIA':
                return render(request, 'menuA.html', datos)
            elif usuario.rol == 'MEDICO':
                return render(request, 'menuM.html', datos)
        else:
            datos = {'r': 'Usuario no encontrado'}
            return render(request, 'login.html', datos)



