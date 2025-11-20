from django.db import models

class Usuario(models.Model):
    correo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=128)

    TIPO_USUARIO = [
        ('TENS', 'tens'),
        ('AMBULANCIA', 'ambulancia'),
        ('MEDICO', 'medico'),
    ]

    rol = models.CharField(max_length=30, choices=TIPO_USUARIO)
    def __str__(self):
        return f"{self.nombre} ({self.correo})"



class Comorbilidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

GENERO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=30)
    edad = models.IntegerField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)

    comorbilidades = models.ManyToManyField(Comorbilidad)

    def __str__(self):

        return f"{self.nombre} (RUT: {self.rut})"

class Derivacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    fecha_ingreso = models.DateField()
    PREVISION_CHOICES = [('FONASA', 'FONASA'), ('ISAPRE', 'ISAPRE')]
    tipo_prevision = models.CharField(max_length=10, choices=PREVISION_CHOICES)
    accidente_laboral = models.BooleanField()
    motivo_derivacion = models.TextField()
    prestacion_requerida = models.TextField()
    GRAVEDAD_CHOICES = [('BAJA', 'Baja'), ('MEDIA', 'Media'), ('ALTA', 'Alta'), ('CRITICA', 'Crítica')]
    gravedad = models.CharField(max_length=10, choices=GRAVEDAD_CHOICES)
    evaluacion = models.TextField()

    def lista_comorbilidades(self):
        return self.paciente.comorbilidades.all()

    def __str__(self):

        return f"Ficha {self.id} de {self.paciente.nombre} (RUT: {self.paciente.rut})"


class HistorialModificacion(models.Model):
    derivacion = models.ForeignKey(
        'Derivacion',
        on_delete=models.CASCADE,
        related_name='historial_modificaciones'
    )
    usuario_modificador = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuario Modificador'
    )

    fecha_modificacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora'
    )



