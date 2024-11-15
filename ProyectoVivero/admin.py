from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Productor

@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('documento_identidad', 'nombre', 'apellido', 'telefono', 'correo')