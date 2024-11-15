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
    
# Modelo Vivero
class Vivero(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, related_name='viveros')
    codigo = models.CharField(max_length=50, unique=True)  # Asegúrate de que unique=True esté presente
    tipo_cultivo = models.CharField(max_length=100)

    def __str__(self):
        return f'Vivero {self.codigo} - {self.tipo_cultivo}'
    
# Clase abstracta ProductoControl
class ProductoControl(models.Model):
    registro_ica = models.CharField(max_length=50)
    nombre_producto = models.CharField(max_length=100)
    frecuencia_aplicacion = models.IntegerField()  # Cada X días
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

# Modelo ProductoControlHongo
class ProductoControlHongo(ProductoControl):
    periodo_carencia = models.IntegerField()  # Días
    nombre_hongo = models.CharField(max_length=100)

    def __str__(self):
        return f'Hongo {self.nombre_hongo} - {self.nombre_producto}'

# Modelo ProductoControlPlaga
class ProductoControlPlaga(ProductoControl):
    periodo_carencia = models.IntegerField()  # Días

    def __str__(self):
        return f'Plaga - {self.nombre_producto}'

# Modelo ProductoControlFertilizante
class ProductoControlFertilizante(ProductoControl):
    fecha_ultima_aplicacion = models.DateField()

    def __str__(self):
        return f'Fertilizante - {self.nombre_producto}'

# Modelo Labor
class Labor(models.Model):
    vivero = models.ForeignKey(Vivero, on_delete=models.CASCADE, related_name='labores')
    fecha = models.DateField()
    descripcion = models.TextField()

    # Relacionamos Labor con los productos que puede utilizar
    productos_control_hongo = models.ManyToManyField(ProductoControlHongo)
    productos_control_plaga = models.ManyToManyField(ProductoControlPlaga)
    productos_control_fertilizante = models.ManyToManyField(ProductoControlFertilizante)

    def __str__(self):
        return f'Labor {self.descripcion} en {self.fecha}'

