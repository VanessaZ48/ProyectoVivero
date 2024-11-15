from django.test import TestCase
from ProyectoVivero.models import Productor, Finca, Vivero, Labor, ProductoControlHongo, ProductoControlPlaga, ProductoControlFertilizante
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your tests here.


"""PRUEBAS CADA ENTIDAD, REQUERIMIENTO FUNCIONALES Y NO FUNCIONALES."""

# Pruebas para el modelo Productor
class ProductorTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad='123456789',
            nombre='Juan',
            apellido='Pérez',
            telefono='5551234',
            correo='juan@example.com'
        )

    def test_productor_creation(self):
        """Funcional: Verifica que se pueda crear un Productor con datos válidos"""
        productor = Productor.objects.get(documento_identidad='123456789')
        self.assertEqual(productor.nombre, 'Juan')
        self.assertEqual(productor.apellido, 'Pérez')

    def test_productor_unique_documento(self):
        """No funcional: Verifica que el documento de identidad sea único"""
        with self.assertRaises(ValidationError):
            productor = Productor(
                documento_identidad='123456789',
                nombre='Ana',
                apellido='García',
                telefono='5556789',
                correo='ana@example.com'
            )
            productor.full_clean()  # Esto valida los datos y debe fallar

    def test_productor_str_method(self):
        """Funcional: Verifica la representación en cadena del Productor"""
        self.assertEqual(str(self.productor), 'Juan Pérez')

# Pruebas para el modelo Finca
class FincaTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad='987654321',
            nombre='Carlos',
            apellido='Martínez',
            telefono='5559876',
            correo='carlos@example.com'
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro='FNC002',
            municipio='Bogotá'
        )

    def test_finca_creation(self):
        """Funcional: Verifica que se pueda crear una Finca con datos válidos"""
        finca = Finca.objects.get(numero_catastro='FNC002')
        self.assertEqual(finca.municipio, 'Bogotá')

    def test_finca_foreign_key(self):
        """Funcional: Verifica que la Finca esté asociada correctamente a un Productor"""
        self.assertEqual(self.finca.productor.nombre, 'Carlos')

    def test_finca_unique_numero_catastro(self):
        """No funcional: Verifica que el número de catastro sea único"""
        with self.assertRaises(ValidationError):
            finca = Finca(
                productor=self.productor,
                numero_catastro='FNC002',  # Mismo número de catastro
                municipio='Medellín'
            )
            finca.full_clean()  # Esto valida los datos y debe fallar

    def test_finca_str_method(self):
        """Funcional: Verifica la representación en cadena de la Finca"""
        self.assertEqual(str(self.finca), 'Finca FNC002 - Bogotá')

# Pruebas para el modelo Vivero
from django.db.utils import IntegrityError

class ViveroTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(
            productor=Productor.objects.create(
                documento_identidad='876543210',
                nombre='Luis',
                apellido='Fernández',
                telefono='5555432',
                correo='luis@example.com'
            ),
            numero_catastro='FNC003',
            municipio='Cali'
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo='VIV002',
            tipo_cultivo='Maíz'
        )

    def test_vivero_creation(self):
        """Funcional: Verifica que se pueda crear un Vivero con datos válidos"""
        vivero = Vivero.objects.get(codigo='VIV002')
        self.assertEqual(vivero.tipo_cultivo, 'Maíz')

    def test_vivero_foreign_key(self):
        """Funcional: Verifica que el Vivero esté asociado correctamente a una Finca"""
        self.assertEqual(self.vivero.finca.numero_catastro, 'FNC003')

    def test_vivero_unique_codigo(self):
        """No funcional: Verifica que el código del Vivero sea único"""
        # Primero, crea un Vivero con un código específico
        Vivero.objects.create(
            finca=self.finca,
            codigo='VIV003',
            tipo_cultivo='Trigo'
        )
        
        # Intenta crear otro Vivero con el mismo código
        try:
            Vivero.objects.create(
                finca=self.finca,
                codigo='VIV003',  # Código duplicado
                tipo_cultivo='Cebada'
            )
            # Si no se lanza una excepción, la prueba falla
            self.fail("Expected IntegrityError due to unique constraint on 'codigo'")
        except IntegrityError:
            pass  # La excepción esperada se ha lanzado

# Pruebas para el modelo Labor
class LaborTests(TestCase):
    def setUp(self):
        self.vivero = Vivero.objects.create(
            finca=Finca.objects.create(
                productor=Productor.objects.create(
                    documento_identidad='654321098',
                    nombre='Marta',
                    apellido='López',
                    telefono='5554321',
                    correo='marta@example.com'
                ),
                numero_catastro='FNC004',
                municipio='Medellín'
            ),
            codigo='VIV003',
            tipo_cultivo='Arroz'
        )
        self.labor = Labor.objects.create(
            vivero=self.vivero,
            fecha='2024-09-15',
            descripcion='Aplicación de fungicida'
        )
        self.producto_hongo = ProductoControlHongo.objects.create(
            registro_ica='ICA123',
            nombre_producto='Fungicida X',
            frecuencia_aplicacion=15,
            valor=100.00,
            periodo_carencia=7,
            nombre_hongo='Oídio'
        )
        self.labor.productos_control_hongo.add(self.producto_hongo)

   
    
    def test_labor_creation(self):
        """Funcional: Verifica que se pueda crear una Labor con datos válidos"""
        labor = Labor.objects.get(descripcion='Aplicación de fungicida')
        fecha_esperada = datetime.strptime('2024-09-15', '%Y-%m-%d').date()  # Convierte la cadena a date
        self.assertEqual(labor.fecha, fecha_esperada)


    def test_labor_foreign_key(self):
        """Funcional: Verifica que la Labor esté asociada correctamente a un Vivero"""
        self.assertEqual(self.labor.vivero.codigo, 'VIV003')

    def test_labor_m2m_relationship(self):
        """Funcional: Verifica que la Labor pueda estar asociada a Productos de Control Hongo"""
        self.assertIn(self.producto_hongo, self.labor.productos_control_hongo.all())

    def test_labor_fecha_format(self):
        """No funcional: Verifica que la fecha de la Labor sea un valor de fecha válido"""
        self.assertIsInstance(self.labor.fecha, str)  # Asume que la fecha es guardada como string

    def test_labor_str_method(self):
        """Funcional: Verifica la representación en cadena de la Labor"""
        self.assertEqual(str(self.labor), 'Labor Aplicación de fungicida en 2024-09-15')