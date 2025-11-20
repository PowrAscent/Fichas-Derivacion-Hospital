from django.shortcuts import render
from gestion.models import Usuario
from gestion.models import Paciente
from gestion.models import Derivacion
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

        print(hashed)

        if usuario:
            request.session['estadoSesion'] = True
            request.session['correo'] = usuario.correo
            request.session['rol'] = usuario.rol
            request.session['id'] = usuario.id

            datos = {'correo' : usuario.correo, 'rol': usuario.rol.lower(),  'r': 'Autenticacion exitosa'}

            print(usuario)

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

def mostrar_registrar(request):
    if request.session.get('estadoSesion') == True:
        return render(request, 'registrar.html')

def registrar(request):
    context = {}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'search':
            rut = request.POST.get('rut', '').strip()
            context['rut_buscado'] = rut

            if rut:
                try:
                    paciente = Paciente.objects.get(rut=rut)
                    context['paciente_encontrado'] = paciente
                    context['comorbilidades_list'] = paciente.comorbilidades.all()
                except Paciente.DoesNotExist:
                    context['r'] = 'Paciente no encontrado.'


        elif action == 'register':
            paciente_id = request.POST.get('paciente_id')


            if not paciente_id:
                context['r'] = 'Error: No se ha encontrado un paciente válido para la derivación.'
                return render(request, 'registrar.html', context)

            try:
                paciente = Paciente.objects.get(pk=paciente_id)
                usuario_id = request.session.get('id')
                usuario_creador = Usuario.objects.get(pk=usuario_id)

                Derivacion.objects.create(
                    paciente=paciente,
                    usuario_creador=usuario_creador,
                    fecha_ingreso=request.POST.get('fecha_ingreso'),
                    tipo_prevision=request.POST.get('prevision'),
                    accidente_laboral=request.POST.get('accidente_laboral') == 'True',
                    motivo_derivacion=request.POST.get('motivo_derivacion'),
                    prestacion_requerida=request.POST.get('prestacion_requerida'),
                    gravedad=request.POST.get('gravedad'),
                    evaluacion=request.POST.get('evaluacion'),
                )
                context['r'] = f'Ficha de derivación registrada con éxito para {paciente.nombre}.'

            except Paciente.DoesNotExist:
                 context['r'] = 'El paciente referenciado no existe.'
            except Exception as e:
                context['r'] = f'Error inesperado: {str(e)}'

        return render(request, 'registrar.html', context)


def modificar(request, id):
    if request.session.get('estadoSesion') == True:
        derivacion = Derivacion.objects.get(id=id)
        context = {
            'derivacion': derivacion,
        }

        if request.method == 'POST':
            try:
                derivacion.fecha_ingreso = request.POST.get('fecha_ingreso')
                derivacion.motivo_derivacion = request.POST.get('motivo_derivacion')
                derivacion.prestacion_requerida = request.POST.get('prestacion_requerida')
                derivacion.gravedad = request.POST.get('gravedad')
                derivacion.evaluacion = request.POST.get('evaluacion')

                derivacion.save()

                context['r'] = f'Ficha de derivación modificada con éxito para {derivacion.paciente.nombre}.'
            except Exception as e:
                context['r'] = f'Error inesperado: {str(e)}'

        return render(request, 'modificar.html', context)

def listar(request):
    if request.session.get('estadoSesion') == True:

        rut_buscado = request.GET.get('rut', '').strip()

        derivaciones = Derivacion.objects.select_related('paciente').all().order_by('-fecha_ingreso')


        if rut_buscado:
            derivaciones = derivaciones.filter(
                paciente__rut__icontains=rut_buscado
            )

        context = {
            'derivaciones': derivaciones,
            'rut_buscado': rut_buscado,
        }



        return render(request, 'listar.html', context)


def detalle_derivacion(request, id):
    if request.session.get('estadoSesion') == True:
        derivacion = Derivacion.objects.get(id=id)
        context = {
            'derivacion': derivacion,
            'comorbilidades': derivacion.paciente.comorbilidades.all(),

        }
        return render(request, 'detalle_derivacion.html', context)