import sys
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import random

from gestion.models import Paciente, Comorbilidad, Usuario, Derivacion



class Command(BaseCommand):
    help = 'Precarga datos iniciales de usuarios, pacientes, comorbilidades y 15 derivaciones.'

    def handle(self, *args, **options):


        usuarios_data = [
            {
                'correo': 'cardio.medico@hrr.cl', 'nombre': 'Dr. Sofía Rojas', 'rol': 'MEDICO',
                'especialidad': 'Cardiología', 'contraseña_plana': 'passcardio'
            },
            {
                'correo': 'bronco.medico@hrr.cl', 'nombre': 'Dr. Jaime Herrera', 'rol': 'MEDICO',
                'especialidad': 'Broncopulmonar', 'contraseña_plana': 'passbronco'
            },
            {
                'correo': 'nefro.medico@hrr.cl', 'nombre': 'Dra. Isabel Mena', 'rol': 'MEDICO',
                'especialidad': 'Nefrología', 'contraseña_plana': 'passnefro'
            },
            {
                'correo': 'tens@hrr.cl', 'nombre': 'Sra. Javiera Cruz', 'rol': 'TENS',
                'especialidad': None, 'contraseña_plana': 'passtens'
            },
            {
                'correo': 'ambulancia@hrr.cl', 'nombre': 'Chofer Juan Pérez', 'rol': 'AMBULANCIA',
                'especialidad': None, 'contraseña_plana': 'passambu'
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
            usuarios_map[user_data['rol']] = usuario
            if user_data['rol'] == 'MEDICO':
                usuarios_map[user_data['especialidad']] = usuario

            if created:
                self.stdout.write(f"  👨‍⚕️ Creado: {usuario.nombre} ({usuario.rol}) - Esp: {especialidad_display}")
            else:
                self.stdout.write(f"  ▶️ Ya existe: {usuario.nombre}")


        medico_cardio = usuarios_map.get('Cardiología')
        medico_bronco = usuarios_map.get('Broncopulmonar')
        medico_nefro = usuarios_map.get('Nefrología')
        usuario_creador = usuarios_map.get('TENS')


        # -----------------------------
        # 2. CREAR COMORBILIDADES BASE
        # -----------------------------

        comorbilidades_data = [
            'Diabetes Tipo II', 'Hipertensión Arterial', 'Asma Bronquial',
            'Insuficiencia Renal Crónica', 'Obesidad Mórbida',
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


        # -----------------------------
        # 3. CREAR PACIENTES (12 PACIENTES)
        # -----------------------------

        pacientes_data = [
            {'rut': '11111111-1', 'nombre': 'Elena Guzmán', 'edad': 68, 'genero': 'F',
             'comorbilidades': ['Diabetes Tipo II', 'Hipertensión Arterial', 'Insuficiencia Cardíaca Congestiva (ICC)']},
            {'rut': '22222222-2', 'nombre': 'Ricardo Soto', 'edad': 45, 'genero': 'M',
             'comorbilidades': ['Obesidad Mórbida', 'Asma Bronquial']},
            {'rut': '33333333-3', 'nombre': 'Carmen Flores', 'edad': 75, 'genero': 'F',
             'comorbilidades': ['Hipertensión Arterial', 'Insuficiencia Renal Crónica']},
            {'rut': '44444444-4', 'nombre': 'Pedro Naranjo', 'edad': 82, 'genero': 'M',
             'comorbilidades': ['EPOC', 'Diabetes Tipo II']},
            {'rut': '55555555-5', 'nombre': 'Teresa Vidal', 'edad': 55, 'genero': 'F',
             'comorbilidades': ['Hipertensión Arterial', 'Obesidad Mórbida']},
            {'rut': '66666666-6', 'nombre': 'José Cárcamo', 'edad': 60, 'genero': 'M',
             'comorbilidades': ['Diabetes Tipo II']},
            {'rut': '77777777-7', 'nombre': 'Andrea Salas', 'edad': 38, 'genero': 'F',
             'comorbilidades': ['Asma Bronquial']},
            {'rut': '88888888-8', 'nombre': 'Luis Rojas', 'edad': 79, 'genero': 'M',
             'comorbilidades': ['Insuficiencia Cardíaca Congestiva (ICC)', 'Hipertensión Arterial']},
            {'rut': '99999999-9', 'nombre': 'Patricia Lira', 'edad': 50, 'genero': 'F',
             'comorbilidades': ['Insuficiencia Renal Crónica']},
            {'rut': '10101010-0', 'nombre': 'Mario Vega', 'edad': 65, 'genero': 'M',
             'comorbilidades': ['EPOC', 'Obesidad Mórbida']},
            {'rut': '11111110-1', 'nombre': 'Silvia Torres', 'edad': 70, 'genero': 'F',
             'comorbilidades': ['Hipertensión Arterial']},
            {'rut': '12121212-2', 'nombre': 'Ramón Ibarra', 'edad': 28, 'genero': 'M',
             'comorbilidades': []},
        ]

        pacientes_map = {}
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreando Pacientes y vinculando Comorbilidades..."))

        for data in pacientes_data:
            comorbilidades_nombres = data.pop('comorbilidades')
            paciente, created = Paciente.objects.get_or_create(rut=data['rut'], defaults=data)
            pacientes_map[data['rut']] = paciente

            comorbilidades_a_vincular = []
            for nombre_com in comorbilidades_nombres:
                # Usar .get() por si se usaron abreviaciones como 'EPOC'
                match_name = next((key for key in comorbilidades_map if nombre_com in key), nombre_com)
                if match_name in comorbilidades_map:
                    comorbilidades_a_vincular.append(comorbilidades_map[match_name])

            paciente.comorbilidades.set(comorbilidades_a_vincular)

            if created:
                self.stdout.write(f"  ✅ Paciente Creado: {paciente.nombre} (Comorbilidades: {', '.join(comorbilidades_nombres)})")
            else:
                self.stdout.write(f"  ▶️ Paciente Actualizado: {paciente.nombre}")


        # -----------------------------
        # 4. CREAR 15 DERIVACIONES REPARTIDAS
        # -----------------------------

        derivaciones_data = [
            # Médico 1: Cardiología (ICC, HTA)
            {'paciente_rut': '11111111-1', 'motivo': 'Dolor torácico atípico, disnea de esfuerzo. ICC descompensada.',
             'req': 'Evaluación cardiológica urgente.', 'gravedad': 'ALTA', 'temp': 36.5, 'pa': '155/95', 'fc': 95, 'fr': 20, 'sato2': 94, 'pendiente': True, 'medico': medico_cardio},
            {'paciente_rut': '88888888-8', 'motivo': 'Edema pulmonar agudo. Crisis hipertensiva.',
             'req': 'Manejo en UPC y monitoreo hemodinámico.', 'gravedad': 'CRITICA', 'temp': 36.8, 'pa': '200/110', 'fc': 110, 'fr': 28, 'sato2': 88, 'pendiente': True, 'medico': medico_cardio},
            {'paciente_rut': '55555555-5', 'motivo': 'Palpitaciones ocasionales. HTA mal controlada.',
             'req': 'Ajuste de medicamentos antihipertensivos.', 'gravedad': 'MEDIA', 'temp': 37.0, 'pa': '160/100', 'fc': 85, 'fr': 18, 'sato2': 96, 'pendiente': True, 'medico': medico_cardio},
            {'paciente_rut': '11111110-1', 'motivo': 'Control rutinario post-IAM. ECG con alteraciones leves.',
             'req': 'Interconsulta no urgente con cardiología.', 'gravedad': 'BAJA', 'temp': 36.6, 'pa': '130/80', 'fc': 70, 'fr': 16, 'sato2': 98, 'pendiente': False, 'medico': medico_cardio}, # APROBADA
            {'paciente_rut': '66666666-6', 'motivo': 'Dolor precordial sin irradiación. Antecedente DM.',
             'req': 'Descarte de síndrome coronario agudo.', 'gravedad': 'ALTA', 'temp': 36.4, 'pa': '140/90', 'fc': 90, 'fr': 22, 'sato2': 93, 'pendiente': True, 'medico': medico_cardio},

            # Médico 2: Broncopulmonar (Asma, EPOC)
            {'paciente_rut': '22222222-2', 'motivo': 'Crisis asmática severa, uso de musculatura accesoria.',
             'req': 'Nebulizaciones continuas y corticoides IV.', 'gravedad': 'CRITICA', 'temp': 37.2, 'pa': '130/85', 'fc': 120, 'fr': 30, 'sato2': 85, 'pendiente': True, 'medico': medico_bronco},
            {'paciente_rut': '44444444-4', 'motivo': 'Exacerbación de EPOC. Tos productiva y fiebre.',
             'req': 'Hospitalización y antibioticoterapia.', 'gravedad': 'ALTA', 'temp': 38.5, 'pa': '145/90', 'fc': 100, 'fr': 25, 'sato2': 90, 'pendiente': True, 'medico': medico_bronco},
            {'paciente_rut': '77777777-7', 'motivo': 'Asma sin control a pesar de inhaladores. Solicitud de test de función pulmonar.',
             'req': 'Cita para espirometría.', 'gravedad': 'MEDIA', 'temp': 36.7, 'pa': '120/75', 'fc': 75, 'fr': 17, 'sato2': 97, 'pendiente': False, 'medico': medico_bronco}, # APROBADA
            {'paciente_rut': '10101010-0', 'motivo': 'Disnea crónica por EPOC. Necesidad de oxigenoterapia domiciliaria.',
             'req': 'Evaluación de gases arteriales y oxigenoterapia.', 'gravedad': 'ALTA', 'temp': 37.0, 'pa': '135/85', 'fc': 80, 'fr': 20, 'sato2': 92, 'pendiente': True, 'medico': medico_bronco},
            {'paciente_rut': '12121212-2', 'motivo': 'Neumonía comunitaria, saturación normal. Requiere alta y seguimiento ambulatorio.',
             'req': 'Revisión de placa torácica y confirmación de alta.', 'gravedad': 'BAJA', 'temp': 37.5, 'pa': '110/70', 'fc': 80, 'fr': 18, 'sato2': 96, 'pendiente': True, 'medico': medico_bronco},

            # Médico 3: Nefrología (IRC, Deshidratación severa)
            {'paciente_rut': '33333333-3', 'motivo': 'Anuria de 24h. Diagnóstico previo de IRC.',
             'req': 'Traslado a unidad de diálisis urgente.', 'gravedad': 'CRITICA', 'temp': 36.3, 'pa': '170/90', 'fc': 88, 'fr': 16, 'sato2': 98, 'pendiente': True, 'medico': medico_nefro},
            {'paciente_rut': '99999999-9', 'motivo': 'Control post-trasplante. Creatinina elevada.',
             'req': 'Biopsia renal de urgencia.', 'gravedad': 'ALTA', 'temp': 37.8, 'pa': '150/95', 'fc': 78, 'fr': 18, 'sato2': 95, 'pendiente': True, 'medico': medico_nefro},
            {'paciente_rut': '66666666-6', 'motivo': 'Cetoacidosis diabética. Deshidratación severa (compartido con cardio, pero enfocado en fluidos).',
             'req': 'Manejo en UCI/UTI, reposición de volumen y electrolitos.', 'gravedad': 'CRITICA', 'temp': 38.0, 'pa': '100/60', 'fc': 130, 'fr': 24, 'sato2': 97, 'pendiente': True, 'medico': medico_nefro},
            {'paciente_rut': '44444444-4', 'motivo': 'Sospecha de infección urinaria complicada en paciente de edad avanzada.',
             'req': 'Cultivo de orina e ingreso para observación.', 'gravedad': 'MEDIA', 'temp': 37.5, 'pa': '130/80', 'fc': 80, 'fr': 18, 'sato2': 96, 'pendiente': False, 'medico': medico_nefro}, # APROBADA
            {'paciente_rut': '11111111-1', 'motivo': 'Hiponatremia asintomática persistente. Necesidad de estudio etiológico.',
             'req': 'Interconsulta electiva con nefrología.', 'gravedad': 'BAJA', 'temp': 36.8, 'pa': '125/75', 'fc': 70, 'fr': 16, 'sato2': 98, 'pendiente': True, 'medico': medico_nefro},
        ]

        total_creadas = 0
        self.stdout.write(self.style.MIGRATE_HEADING("\nCreando 15 Fichas de Derivación..."))

        for i, data in enumerate(derivaciones_data):
            paciente = pacientes_map.get(data['paciente_rut'])
            medico = data['medico']

            # Simular fecha de ingreso reciente (últimos 7 días)
            fecha_ingreso_simulada = timezone.now().date() - timedelta(days=random.randint(0, 7))

            # Asignar una previsión
            prevision = random.choice(['FONASA', 'ISAPRE', 'PARTICULAR'])

            derivacion, created = Derivacion.objects.get_or_create(
                paciente=paciente,
                motivo_derivacion=data['motivo'],
                defaults={
                    'usuario_creador': usuario_creador,
                    'fecha_ingreso': fecha_ingreso_simulada,
                    'tipo_prevision': prevision,
                    'accidente_laboral': random.choice([True, False]),
                    'prestacion_requerida': data['req'],
                    'gravedad': data['gravedad'],
                    'evaluacion': f'Paciente en manejo inicial por {usuario_creador.nombre}. Se requiere cupo y revisión por especialista.',
                    'temperatura': data['temp'],
                    'presion_arterial': data['pa'],
                    'frecuencia_cardiaca': data['fc'],
                    'frecuencia_respiratoria': data['fr'],
                    'saturacion_oxigeno': data['sato2'],
                    'antecedentes': 'Datos recogidos en terreno. Se adjunta ficha. - Ant: Sin registro',
                    'alergias': 'Negadas',
                    'pendiente': data['pendiente'],
                    'medico_asignado': medico,

                }
            )

            if created:
                estado = "PENDIENTE" if data['pendiente'] else "APROBADA"
                self.stdout.write(f"  🩺 Creada Derivación #{derivacion.id}: {paciente.nombre} -> {medico.nombre} ({estado})")
                total_creadas += 1

        self.stdout.write(self.style.SUCCESS(f'\nDatos de prueba cargados con éxito! ({total_creadas} derivaciones creadas/actualizadas)'))