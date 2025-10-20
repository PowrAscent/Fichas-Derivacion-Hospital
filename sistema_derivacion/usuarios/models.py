from django.db import models

class Usuario(models.Model):
    correo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=30)
    contraseña = models.CharField(max_length=32)

def __str__(self):
    return str(self.correo)+"-"+str(self.nombre)+"-"+str(self.contraseña)