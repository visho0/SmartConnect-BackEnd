from django.core.management.base import BaseCommand
from core.models import Usuario, Departamento, Barrera

class Command(BaseCommand):
    help = 'Crea datos iniciales para el sistema'

    def handle(self, *args, **options):
        # Crear usuario admin
        if not Usuario.objects.filter(username='admin').exists():
            admin = Usuario.objects.create_user(
                username='admin',
                email='admin@smartconnect.com',
                password='admin123',
                rol='admin',
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario admin creado: {admin.username}'))
        
        # Crear usuario operador
        if not Usuario.objects.filter(username='operador').exists():
            operador = Usuario.objects.create_user(
                username='operador',
                email='operador@smartconnect.com',
                password='operador123',
                rol='operador',
                first_name='Operador',
                last_name='Sistema'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario operador creado: {operador.username}'))
        
        # Crear departamento por defecto
        depto, created = Departamento.objects.get_or_create(
            nombre='Recepción',
            defaults={'descripcion': 'Área de recepción principal'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Departamento creado: {depto.nombre}'))
        
        # Crear barrera por defecto
        barrera, created = Barrera.objects.get_or_create(
            nombre='Barrera Principal',
            defaults={'departamento': depto, 'estado': 'cerrada'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Barrera creada: {barrera.nombre}'))
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales creados correctamente'))

