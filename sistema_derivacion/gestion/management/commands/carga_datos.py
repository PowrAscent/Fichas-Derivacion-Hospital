import sys
from django.core.management.base import BaseCommand
# Importamos make_password para hashear contraseñas
from django.contrib.auth.hashers import make_password
from gestion.models import Paciente, Comorbilidad, Usuario # Importamos el modelo Usuario

class Command(BaseCommand):
    help = 'Precarga datos iniciales de usuarios, pacientes y comorbilidades.'

    def handle(self, *args, **options):
        # -----------------------------
        # 1. CREAR USUARIOS DE PRUEBA
        # -----------------------------
        usuarios_data = [
            {
                'correo': 'medico@hrr.cl',
                'nombre': 'Dr. Andrés Bello',
                'rol': 'MEDICO',
                'contraseña_plana': 'passmedico'
            },
            {
                'correo': 'tens@hrr.cl',
                'nombre': 'Sra. Javiera Cruz',
                'rol': 'TENS',
                'contraseña_plana': 'passtens'
            },
            {
                'correo': 'ambulancia@hrr.cl',
                'nombre': 'Chofer Juan Pérez',
                'rol': 'AMBULANCIA',
                'contraseña_plana': 'passambu'
            },
        ]

        usuarios_map = {}
        self.stdout.write(self.style.MIGRATE_HEADING("Creando Usuarios de Prueba..."))

        for user_data in usuarios_data:
            contraseña_hash = make_password(user_data['contraseña_plana'])

            # get_or_create para el usuario
            usuario, created = Usuario.objects.get_or_create(
                correo=user_data['correo'],
                defaults={
                    'nombre': user_data['nombre'],
                    'rol': user_data['rol'],
                    'contraseña': contraseña_hash
                }
            )
            usuarios_map[user_data['rol']] = usuario

            if created:
                self.stdout.write(f"  👨‍⚕️ Creado: {usuario.nombre} ({usuario.rol})")
            else:
                self.stdout.write(f"  ▶️ Ya existe: {usuario.nombre}")


        # -----------------------------
        # 2. CREAR COMORBILIDADES BASE
        # -----------------------------

        # Lista de comorbilidades a crear
        comorbilidades_data = [
            'Diabetes Tipo II',
            'Hipertensión Arterial',
            'Asma Bronquial',
            'Insuficiencia Renal Crónica',
            'Obesidad Mórbida',
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

        # -----------------------------
        # 3. CREAR PACIENTES Y VINCULAR COMORBILIDADES
        # -----------------------------

        pacientes_data = [
            {
                'rut': '11111111-1',
                'nombre': 'Elena Guzmán',
                'edad': 68,
                'genero': 'F',
                'comorbilidades': ['Diabetes Tipo II', 'Hipertensión Arterial']
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
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("\nCreando Pacientes y vinculando Comorbilidades..."))

        for data in pacientes_data:
            comorbilidades_nombres = data.pop('comorbilidades')

            # Crear o actualizar el paciente
            paciente, created = Paciente.objects.get_or_create(rut=data['rut'], defaults=data)

            # VINCULAR CON COMORBILIDADES
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