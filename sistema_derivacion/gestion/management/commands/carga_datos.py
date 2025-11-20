import sys
from django.core.management.base import BaseCommand
from gestion.models import Paciente, Comorbilidad # Asegúrate de importar tus modelos

class Command(BaseCommand):
    help = 'Precarga datos iniciales de pacientes y comorbilidades.'

    def handle(self, *args, **options):
        # -----------------------------
        # 1. CREAR COMORBILIDADES BASE
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
        self.stdout.write(self.style.MIGRATE_HEADING("Creando Comorbilidades..."))

        for nombre in comorbilidades_data:
            # get_or_create previene duplicados si el comando se ejecuta más de una vez
            comorbilidad, created = Comorbilidad.objects.get_or_create(nombre=nombre)
            comorbilidades_map[nombre] = comorbilidad
            if created:
                self.stdout.write(f"  ✅ Creada: {nombre}")
            else:
                self.stdout.write(f"  ▶️ Ya existe: {nombre}")

        # -----------------------------
        # 2. CREAR PACIENTES Y VINCULAR COMORBILIDADES
        # -----------------------------

        # Datos de pacientes con las comorbilidades a asignar
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

            # 3. VINCULAR CON COMORBILIDADES (Many-to-Many)
            comorbilidades_a_vincular = []
            for nombre_com in comorbilidades_nombres:
                if nombre_com in comorbilidades_map:
                    comorbilidades_a_vincular.append(comorbilidades_map[nombre_com])

            # Asignar la lista de objetos de Comorbilidad al paciente
            paciente.comorbilidades.set(comorbilidades_a_vincular)

            if created:
                self.stdout.write(f"  ✅ Paciente Creado: {paciente.nombre} (Comorbilidades: {', '.join(comorbilidades_nombres)})")
            else:
                self.stdout.write(f"  ▶️ Paciente Actualizado: {paciente.nombre} (Comorbilidades actualizadas)")


        self.stdout.write(self.style.SUCCESS('\nDatos iniciales de pacientes y comorbilidades cargados con éxito!'))