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

            datos = {'correo' : usuario.correo, 'rol': usuario.rol.lower(),  'r': 'Autenticacion exitosa'}

            if usuario.rol == 'TENS':
                return render(request, 'menuA.html', datos)
            elif usuario.rol == 'AMBULANCIA':
                return render(request, 'menuA.html', datos)
            elif usuario.rol == 'MEDICO':
                return render(request, 'menuA.html', datos)
        else:
            datos = {'rd': 'Usuario no encontrado', 'img1' : 'logo_rancagua.png'}
            return render(request, 'login.html', datos)
    else:
        datos = {'img1' : 'logo_rancagua.png'}
        return render(request, 'login.html', datos)


def logout(request):
    try:
        del request.session['estadoSesion']
        del request.session['correo']
        del request.session['rol']
        datos = {'rs':'Sesion cerrada correctamente!', 'img1' : 'logo_rancagua.png'}
        return render(request, 'login.html', datos)
    except:
        datos = {'rd':'La sesion ya está cerrada!', 'img1' : 'logo_rancagua.png'}
        return render(request, 'login.html', datos)

def panel(request):
    if request.session.get('estadoSesion') == True:
        datos = {
            'correo': request.session.get('correo'),
            'rol': request.session.get('rol').lower()
        }
        return render(request, 'menuA.html', datos)

def registrar(request):
    if request.session.get('estadoSesion') == True:
        datos = {
            'correo': request.session.get('correo'),
            'rol': request.session.get('rol').lower(),
        }
        if request.method == 'POST':
            datos['r'] = 'Ficha registrada con exito'
            return render(request, 'registrar.html', datos)
        return render(request, 'registrar.html', datos)

def modificar(request):
    if 'estadoSesion' in request.session:
        # r = None
        datos = {
            'correo': request.session.get('correo'),
            'rol': request.session.get('rol').lower()
        }
        if request.method == 'POST':
            datos['r'] = 'Ficha modificada con exito'
            return render(request, 'modificar.html', datos)

        return render(request, 'modificar.html', datos)

def listar(request):
    if 'estadoSesion' in request.session:
        # Simulando datos de paciente y derivaciones (estos datos serán estáticos solo para maquetado)
        paciente = {
            'rut': '12.345.678-9',
            'nombre': 'Juan Pérez',
            'edad': 30,
            'genero': 'Masculino',
            'comorbilidades': 'Hipertensión',
            'funcionalidad': 'Independiente'
        }

        derivaciones = [
            {
                'id':1,
                'fecha_ingreso': '2025-10-22',
                'tipo_prevision': 'Fonasa',
                'accidente_laboral': 'No',
                'motivo_derivacion': 'Dolor torácico',
                'prestacion_requerida': 'Ecocardiograma',
                'evaluacion': 'Estable, control ambulatorio',
                'estado': 'Registrada'
            },
            {
                'id':2,
                'fecha_ingreso': '2025-10-23',
                'tipo_prevision': 'Isapre',
                'accidente_laboral': 'Sí',
                'motivo_derivacion': 'Fractura de pierna',
                'prestacion_requerida': 'Radiografía',
                'evaluacion': 'Urgente, en espera de cirugía',
                'estado': 'En traslado'
            }
        ]

        datos = {
            'correo': request.session.get('correo'),
            'rol': request.session.get('rol').lower(),
            'paciente': paciente,
            'derivaciones': derivaciones
        }

        return render(request, 'listar.html', datos)

"""def listar(request):
    if 'estadoSesion' in request.session:
        datos = {
            'correo': request.session.get('correo'),
            'rol': request.session.get('rol').lower(),
        }
        return render(request, 'listar.html', datos)
"""