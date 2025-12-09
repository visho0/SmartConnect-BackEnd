from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError as DjangoValidationError

# Modelo de Usuario personalizado con roles
class Usuario(AbstractUser):
    ADMIN = 'admin'
    OPERADOR = 'operador'
    
    ROL_CHOICES = [
        (ADMIN, 'Administrador'),
        (OPERADOR, 'Operador'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default=OPERADOR,
        verbose_name='Rol'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

# Modelo de Departamento/Zona
class Departamento(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre del Departamento',
        unique=True
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

# Modelo de Sensor RFID
class Sensor(models.Model):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'
    BLOQUEADO = 'bloqueado'
    PERDIDO = 'perdido'
    
    ESTADO_CHOICES = [
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (BLOQUEADO, 'Bloqueado'),
        (PERDIDO, 'Perdido'),
    ]
    
    codigo_uid = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Código UID/MAC',
        help_text='Identificador único del sensor RFID'
    )
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre del Sensor'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ACTIVO,
        verbose_name='Estado'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        verbose_name='Departamento'
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sensores',
        verbose_name='Usuario Asociado'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['codigo_uid']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_uid})"
    
    def clean(self):
        # Validar que el código UID/MAC tenga formato válido
        if self.codigo_uid and len(self.codigo_uid) < 4:
            raise DjangoValidationError({'codigo_uid': 'El código UID/MAC debe tener al menos 4 caracteres.'})

# Modelo de Barrera
class Barrera(models.Model):
    ABIERTA = 'abierta'
    CERRADA = 'cerrada'
    
    ESTADO_CHOICES = [
        (ABIERTA, 'Abierta'),
        (CERRADA, 'Cerrada'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        verbose_name='Nombre de la Barrera',
        default='Barrera Principal'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=CERRADA,
        verbose_name='Estado'
    )
    departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='barreras',
        verbose_name='Departamento'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    ultima_apertura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Barrera'
        verbose_name_plural = 'Barreras'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_estado_display()}"

# Modelo de Evento de Acceso
class Evento(models.Model):
    PERMITIDO = 'permitido'
    DENEGADO = 'denegado'
    
    TIPO_CHOICES = [
        (PERMITIDO, 'Permitido'),
        (DENEGADO, 'Denegado'),
    ]
    
    AUTOMATICO = 'automatico'
    MANUAL = 'manual'
    
    ORIGEN_CHOICES = [
        (AUTOMATICO, 'Automático (Sensor)'),
        (MANUAL, 'Manual (API)'),
    ]
    
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='eventos',
        verbose_name='Sensor'
    )
    barrera = models.ForeignKey(
        Barrera,
        on_delete=models.CASCADE,
        related_name='eventos',
        verbose_name='Barrera'
    )
    tipo_acceso = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Acceso'
    )
    origen = models.CharField(
        max_length=20,
        choices=ORIGEN_CHOICES,
        default=AUTOMATICO,
        verbose_name='Origen'
    )
    usuario_operador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eventos_operados',
        verbose_name='Usuario Operador'
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    fecha_evento = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del Evento')
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['fecha_evento']),
            models.Index(fields=['tipo_acceso']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_acceso_display()} - {self.barrera.nombre} - {self.fecha_evento}"
