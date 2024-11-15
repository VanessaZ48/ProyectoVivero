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
