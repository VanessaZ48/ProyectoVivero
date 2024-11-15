from django.db import models

# Modelo Productor
class Productor(models.Model):
    documento_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Modelo Finca
class Finca(models.Model):
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE, related_name='fincas')
    numero_catastro = models.CharField(max_length=50, unique=True)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f'Finca {self.numero_catastro} - {self.municipio}'