import sys
from django.core.management.base import BaseCommand
# Importamos make_password para hashear contraseñas
from django.contrib.auth.hashers import make_password
# Asegúrate de que tu modelo Usuario tiene el campo 'especialidad'
from gestion.models import Paciente, Comorbilidad, Usuario

class Command(BaseCommand):
    help = 'Precarga datos iniciales de usuarios, pacientes y comorbilidades.'

    def handle(self, *args, **options):


        usuarios_data = [

            {
                'correo': 'cardio.medico@hrr.cl',
                'nombre': 'Dr. Sofía Rojas',
                'rol': 'MEDICO',
                'especialidad': 'Cardiología',
                'contraseña_plana': 'passcardio'
            },
            {
                'correo': 'bronco.medico@hrr.cl',
                'nombre': 'Dr. Jaime Herrera',
                'rol': 'MEDICO',
                'especialidad': 'Broncopulmonar',
                'contraseña_plana': 'passbronco'
            },
            {
                'correo': 'nefro.medico@hrr.cl',
                'nombre': 'Dra. Isabel Mena',
                'rol': 'MEDICO',
                'especialidad': 'Nefrología',
                'contraseña_plana': 'passnefro'
            },

            {
                'correo': 'tens@hrr.cl',
                'nombre': 'Sra. Javiera Cruz',
                'rol': 'TENS',
                'especialidad': None,
                'contraseña_plana': 'passtens'
            },
            {
                'correo': 'ambulancia@hrr.cl',
                'nombre': 'Chofer Juan Pérez',
                'rol': 'AMBULANCIA',
                'especialidad': None,
                'contraseña_plana': 'passambu'
            },

        ]

        usuarios_map = {}
        self.stdout.write(self.style.MIGRATE_HEADING("Creando Usuarios de Prueba (con Especialidad)..."))

        for user_data in usuarios_data:
            contraseña_hash = make_password(user_data['contraseña_plana'])


            especialidad_display = user_data.get('especialidad') or ''


            usuario, created = Usuario.objects.get_or_create(
                correo=user_data['correo'],
                defaults={
                    'nombre': user_data['nombre'],
                    'rol': user_data['rol'],
                    'especialidad': especialidad_display,
                    'contraseña': contraseña_hash
                }
            )
            usuarios_map[user_data['correo']] = usuario

            if created:
                self.stdout.write(f"  👨‍⚕️ Creado: {usuario.nombre} ({usuario.rol}) - Esp: {especialidad_display}")
            else:
                self.stdout.write(f"  ▶️ Ya existe: {usuario.nombre}")



        comorbilidades_data = [
            'Diabetes Tipo II',
            'Hipertensión Arterial',
            'Asma Bronquial',
            'Insuficiencia Renal Crónica',
            'Obesidad Mórbida',
            'Enfermedad Pulmonar Obstructiva Crónica (EPOC)',
            'Insuficiencia Cardíaca Congestiva (ICC)',
        ]

        comorbilidades_map = {}
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreando Comorbilidades..."))

        for nombre in comorbilidades_data:
            comorbilidad, created = Comorbilidad.objects.get_or_create(nombre=nombre)
            comorbilidades_map[nombre] = comorbilidad
            if created:
                self.stdout.write(f"  ✅ Creada: {nombre}")
            else:
                self.stdout.write(f"  ▶️ Ya existe: {nombre}")



        pacientes_data = [
            {
                'rut': '11111111-1',
                'nombre': 'Elena Guzmán',
                'edad': 68,
                'genero': 'F',
                'comorbilidades': ['Diabetes Tipo II', 'Hipertensión Arterial', 'Insuficiencia Cardíaca Congestiva (ICC)']
            },
            {
                'rut': '22222222-2',
                'nombre': 'Ricardo Soto',
                'edad': 45,
                'genero': 'M',
                'comorbilidades': ['Obesidad Mórbida', 'Asma Bronquial']
            },
            {
                'rut': '33333333-3',
                'nombre': 'Carmen Flores',
                'edad': 75,
                'genero': 'F',
                'comorbilidades': ['Hipertensión Arterial', 'Insuficiencia Renal Crónica']
            },
            {
                'rut': '44444444-4',
                'nombre': 'Pedro Naranjo',
                'edad': 82,
                'genero': 'M',
                'comorbilidades': ['Enfermedad Pulmonar Obstructiva Crónica (EPOC)', 'Diabetes Tipo II']
            },
            {
                'rut': '55555555-5',
                'nombre': 'Teresa Vidal',
                'edad': 55,
                'genero': 'F',
                'comorbilidades': ['Hipertensión Arterial', 'Obesidad Mórbida']
            },
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("\nCreando Pacientes y vinculando Comorbilidades..."))

        for data in pacientes_data:
            comorbilidades_nombres = data.pop('comorbilidades')


            paciente, created = Paciente.objects.get_or_create(rut=data['rut'], defaults=data)


            comorbilidades_a_vincular = []
            for nombre_com in comorbilidades_nombres:
                if nombre_com in comorbilidades_map:
                    comorbilidades_a_vincular.append(comorbilidades_map[nombre_com])

            paciente.comorbilidades.set(comorbilidades_a_vincular)

            if created:
                self.stdout.write(f"  ✅ Paciente Creado: {paciente.nombre} (Comorbilidades: {', '.join(comorbilidades_nombres)})")
            else:
                self.stdout.write(f"  ▶️ Paciente Actualizado: {paciente.nombre}")


        self.stdout.write(self.style.SUCCESS('\nDatos iniciales de prueba cargados con éxito!'))