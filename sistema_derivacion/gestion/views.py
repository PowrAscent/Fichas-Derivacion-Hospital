from django.shortcuts import render
from gestion.models import Usuario
from gestion.models import Paciente
from gestion.models import Derivacion
from gestion.models import HistorialModificacion
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.core.paginator import Paginator
import hashlib

# Create your views here.
def login(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contraseña_plana = request.POST.get('contraseña')

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            usuario = None

        if usuario:
            if check_password(contraseña_plana, usuario.contraseña):

                request.session['estadoSesion'] = True
                request.session['correo'] = usuario.correo
                request.session['rol'] = usuario.rol
                request.session['id'] = usuario.id

                datos = {
                    'correo': usuario.correo,
                    'rol': usuario.rol.lower(),
                    'r': 'Autenticacion exitosa'
                }

                print(f"Usuario logueado: {usuario.nombre} ({usuario.rol})")

                return render(request, 'menuA.html', datos)

            else:
                datos = {'rd': 'Contraseña incorrecta', 'img1': 'logo_rancagua.png'}
                return render(request, 'login.html', datos)

        else:
            datos = {'rd': 'Credenciales incorrectas', 'img1': 'logo_rancagua.png'}
            return render(request, 'login.html', datos)

    datos = {'img1': 'logo_rancagua.png'}
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
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

    datos = {
        'correo': request.session.get('correo'),
        'rol': request.session.get('rol').lower()
    }
    return render(request, 'menuA.html', datos)


def registrar(request):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

    context = {}

    medicos = Usuario.objects.filter(rol='MEDICO')

    context['medicos'] = medicos

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
                    paciente = paciente,
                    usuario_creador = usuario_creador,
                    fecha_ingreso = request.POST.get('fecha_ingreso'),
                    tipo_prevision = request.POST.get('prevision'),
                    accidente_laboral = request.POST.get('accidente_laboral') == 'True',
                    motivo_derivacion = request.POST.get('motivo_derivacion'),
                    prestacion_requerida=request.POST.get('prestacion_requerida'),
                    gravedad = request.POST.get('gravedad'),
                    evaluacion = request.POST.get('evaluacion'),
                    antecedentes = request.POST.get('antecedentes'),
                    alergias = request.POST.get('alergias'),
                    presion_arterial = request.POST.get('csv'),
                    frecuencia_cardiaca = request.POST.get('fc'),
                    temperatura = request.POST.get('temperatura'),
                    frecuencia_respiratoria = request.POST.get('fr'),
                    saturacion_oxigeno = request.POST.get('sato2'),
                    medico_asignado_id = request.POST.get('medico'),
                )
                context['r'] = f'Ficha de derivación registrada con éxito para {paciente.nombre}.'

            except Paciente.DoesNotExist:
                 context['r'] = 'El paciente referenciado no existe.'
            except Exception as e:
                context['r'] = f'Error inesperado: {str(e)}'

        return render(request, 'registrar.html', context)

    return render(request, 'registrar.html', context)


def modificar(request, id):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')


    derivacion = Derivacion.objects.get(id=id)
    medicos = Usuario.objects.filter(rol='MEDICO')


    context = {
        'derivacion': derivacion,
        'medicos': medicos
    }

    print(derivacion)

    if request.method == 'POST':
        try:

            derivacion.fecha_ingreso = request.POST.get('fecha_ingreso')
            derivacion.motivo_derivacion = request.POST.get('motivo_derivacion')
            derivacion.prestacion_requerida = request.POST.get('prestacion_requerida')
            derivacion.gravedad = request.POST.get('gravedad')
            derivacion.evaluacion = request.POST.get('evaluacion')
            derivacion.antecedentes = request.POST.get('antecedentes')
            derivacion.alergias = request.POST.get('alergias')
            derivacion.presion_arterial = request.POST.get('csv')
            derivacion.frecuencia_cardiaca = request.POST.get('fc')
            derivacion.temperatura = request.POST.get('temperatura')
            derivacion.frecuencia_respiratoria = request.POST.get('fr')
            derivacion.saturacion_oxigeno = request.POST.get('sato2')
            derivacion.medico_asignado_id = request.POST.get('medico')
            derivacion.save()

            usuario_id = request.session.get('id')
            usuario_modificador = Usuario.objects.get(pk=usuario_id)
            HistorialModificacion.objects.create(
                derivacion=derivacion,
                usuario_modificador=usuario_modificador
            )

            context['r'] = f'Ficha de derivación modificada con éxito para {derivacion.paciente.nombre}.'
        except Exception as e:
            context['r'] = f'Error inesperado: {str(e)}'

    return render(request, 'modificar.html', context)

def listar(request):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

    rut_buscado = request.GET.get('rut', '').strip()

    derivaciones = Derivacion.objects.select_related('paciente').all().order_by('-fecha_ingreso')

    if rut_buscado:
        derivaciones = derivaciones.filter(paciente__rut__icontains=rut_buscado)

    paginator = Paginator(derivaciones, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'derivaciones': page_obj,
        'rut_buscado': rut_buscado,
        'page_obj': page_obj
    }

    return render(request, 'listar.html', context)


def detalle_derivacion(request, id):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

    derivacion = Derivacion.objects.get(id=id)
    context = {
        'derivacion': derivacion,
        'comorbilidades': derivacion.paciente.comorbilidades.all(),
    }
    return render(request, 'detalle_derivacion.html', context)

def listar_pacientes(request):
    if request.session.get('estadoSesion') != True or request.session.get('rol') != 'MEDICO':
        return redirect('/login/')

    rut_buscado = request.GET.get('rut', '').strip()

    pacientes = Paciente.objects.all().prefetch_related('comorbilidades').order_by('id')

    if rut_buscado:
        pacientes = pacientes.filter(rut__icontains=rut_buscado)

    #Paginador aquiiiiiiii !
    paginator = Paginator(pacientes, 3) #aqui como hay pocos pacientes puse 3
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'pacientes': page_obj, #se cambió pacientes por page_obj
        'rut_buscado': rut_buscado,
        'page_obj': page_obj,
    }

    #fin paginador
    return render(request, 'listar_pacientes.html', context)

def historial_derivaciones(request, id):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

    paciente = Paciente.objects.get(id=id)
    derivaciones = Derivacion.objects.filter(paciente=paciente).order_by('-fecha_ingreso')

    #paginador

    paginator = Paginator(derivaciones, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'derivaciones': page_obj, #derivaciones por page_obj
        'comorbilidades': paciente.comorbilidades.all(),
        'paciente': paciente,
        'page_obj': page_obj
    #fin pagiandor
    }
    return render(request, 'historial_paciente.html', context)
def derivaciones_pendientes(request):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')


    medico_id = request.session.get('id')


    derivaciones = Derivacion.objects.filter(
        pendiente=True,
        medico_asignado_id=medico_id
    ).order_by('fecha_creacion')

    rut_buscado = request.GET.get('rut', ''). strip()
    if rut_buscado != '':
        derivaciones = derivaciones.filter(
            paciente__rut__icontains=rut_buscado
        )
    #PAGINADOR aqui abajooooo!!! ---------------INICIO
    paginator = Paginator (derivaciones, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'derivaciones': page_obj, #SE CAMBIO derivaciones POR page_obj
        'rut_buscado': rut_buscado,
        'page_obj': page_obj,
    }

    return render(request, 'derivaciones_pendientes.html', context)
#PAGINADOR --------------------------FIN

def revisar_derivacion(request, id):
    if request.session.get('estadoSesion') != True:
        return redirect('/login/')

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
            derivacion.antecedentes = request.POST.get('antecedentes')
            derivacion.alergias = request.POST.get('alergias')
            derivacion.presion_arterial = request.POST.get('csv')
            derivacion.frecuencia_cardiaca = request.POST.get('fc')
            derivacion.temperatura = request.POST.get('temperatura')
            derivacion.frecuencia_respiratoria = request.POST.get('fr')
            derivacion.saturacion_oxigeno = request.POST.get('sato2')
            derivacion.medico_asignado_id = request.POST.get('medico')

            aprobacion = request.POST.get('aprobacion')

            context['r'] = f'Ficha de derivación modificada con éxito para {derivacion.paciente.nombre}.'
            if aprobacion == 'pendiente':
                derivacion.pendiente = True
            else:
                derivacion.pendiente = False
                context['r'] = f'Ficha de derivación aprobada con éxito para {derivacion.paciente.nombre}.'

            derivacion.save()

            usuario_id = request.session.get('id')
            usuario_modificador = Usuario.objects.get(pk=usuario_id)
            HistorialModificacion.objects.create(
                derivacion=derivacion,
                usuario_modificador=usuario_modificador
            )

        except Exception as e:
            context['r'] = f'Error inesperado: {str(e)}'

    return render(request, 'revisar_derivacion.html', context)


def asignar_camas(request, id):
    camas = [
        {"id": 1, "sala": "UCI", "cama": "C-01", "estado": "DISPONIBLE"},
        {"id": 2, "sala": "UCI", "cama": "C-02", "estado": "OCUPADA"},
        {"id": 3, "sala": "UCI", "cama": "C-03", "estado": "DISPONIBLE"},
        {"id": 4, "sala": "Medicina", "cama": "M-12", "estado": "OCUPADA"},
        {"id": 5, "sala": "Medicina", "cama": "M-13", "estado": "DISPONIBLE"},
        {"id": 6, "sala": "Trauma", "cama": "T-03", "estado": "DISPONIBLE"},
    ]

    return render(request, "asignar_camas.html", {
        "camas": camas,
        "derivacion_id": id 
    })

