from django.db import models

class Usuario(models.Model):
    correo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=32)

    TIPO_USUARIO = [
        ('TENSOR', 'tens'),
        ('AMBULANCIA', 'ambulancia'),
        ('MEDICO', 'medico'),
    ]

    rol = models.CharField(max_length=30, choices=TIPO_USUARIO)

