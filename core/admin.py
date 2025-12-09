from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Departamento, Sensor, Barrera, Evento

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'rol', 'first_name', 'last_name', 'is_active']
    list_filter = ['rol', 'is_active', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol',)}),
    )

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'fecha_creacion']
    search_fields = ['nombre']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['codigo_uid', 'nombre', 'estado', 'departamento', 'usuario', 'fecha_registro']
    list_filter = ['estado', 'departamento']
    search_fields = ['codigo_uid', 'nombre']

@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'departamento', 'ultima_apertura']
    list_filter = ['estado', 'departamento']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['tipo_acceso', 'barrera', 'sensor', 'origen', 'fecha_evento']
    list_filter = ['tipo_acceso', 'origen', 'fecha_evento']
    readonly_fields = ['fecha_evento']
