from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from django.http import JsonResponse

from .models import Usuario, Departamento, Sensor, Barrera, Evento
from .serializers import (
    UsuarioSerializer, UsuarioListSerializer,
    DepartamentoSerializer,
    SensorSerializer,
    BarreraSerializer,
    EventoSerializer,
    AccesoSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdmin


# Vista de bienvenida en la raíz
@api_view(['GET'])
@permission_classes([AllowAny])
def root_view(request):
    """
    Vista de bienvenida en la raíz del sitio
    """
    return Response({
        "mensaje": "Bienvenido a SmartConnect API",
        "version": "1.0",
        "endpoints": {
            "informacion": "/api/info/",
            "autenticacion": {
                "login": "/api/token/",
                "refresh": "/api/token/refresh/"
            },
            "recursos": {
                "usuarios": "/api/usuarios/",
                "departamentos": "/api/departamentos/",
                "sensores": "/api/sensores/",
                "barreras": "/api/barreras/",
                "eventos": "/api/eventos/"
            }
        },
        "documentacion": "Consulta el README.md para más información sobre los endpoints",
        "nota": "La mayoría de endpoints requieren autenticación JWT. Usa /api/token/ para obtener un token."
    })


# Vista de información del proyecto
@api_view(['GET'])
@permission_classes([AllowAny])
def info_view(request):
    """
    Endpoint /api/info/ - Información del proyecto (sin autenticación requerida)
    """
    return Response({
        "autor": ["Tu Nombre"],  # Cambiar por tu nombre
        "asignatura": "Programación Back End",
        "proyecto": "SmartConnect API",
        "descripcion": "API RESTful para sistema de control de acceso inteligente con sensores RFID, gestión de usuarios, departamentos, barreras y eventos de acceso. Diseñada para integración con aplicaciones móviles e IoT.",
        "version": "1.0"
    })


# Handlers para errores 404 y 500
def custom_404(request, exception):
    return JsonResponse({
        'error': True,
        'message': 'Ruta no encontrada',
        'details': {'path': request.path, 'method': request.method}
    }, status=404)

def custom_500(request):
    return JsonResponse({
        'error': True,
        'message': 'Error interno del servidor',
        'details': {}
    }, status=500)


# Vista personalizada de Token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ViewSets
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [IsAdmin]  # Solo admin puede gestionar usuarios
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UsuarioListSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario autenticado"""
        serializer = UsuarioListSerializer(request.user)
        return Response(serializer.data)


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAdminOrReadOnly]


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.select_related('departamento', 'usuario').all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado de un sensor"""
        sensor = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in dict(Sensor.ESTADO_CHOICES):
            return Response({
                'error': True,
                'message': 'Estado inválido',
                'details': {'estado': f'Debe ser uno de: {", ".join([e[0] for e in Sensor.ESTADO_CHOICES])}'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        sensor.estado = nuevo_estado
        sensor.save()
        
        serializer = self.get_serializer(sensor)
        return Response(serializer.data)


class BarreraViewSet(viewsets.ModelViewSet):
    queryset = Barrera.objects.select_related('departamento').all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def abrir(self, request, pk=None):
        """Abrir barrera manualmente"""
        barrera = self.get_object()
        barrera.estado = Barrera.ABIERTA
        barrera.ultima_apertura = timezone.now()
        barrera.save()
        
        # Registrar evento manual
        Evento.objects.create(
            barrera=barrera,
            tipo_acceso=Evento.PERMITIDO,
            origen=Evento.MANUAL,
            usuario_operador=request.user,
            observaciones='Apertura manual desde API'
        )
        
        serializer = self.get_serializer(barrera)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cerrar barrera manualmente"""
        barrera = self.get_object()
        barrera.estado = Barrera.CERRADA
        barrera.save()
        
        serializer = self.get_serializer(barrera)
        return Response(serializer.data)


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.select_related('sensor', 'barrera', 'usuario_operador').all()
    serializer_class = EventoSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['post'])
    def intentar_acceso(self, request):
        """
        Simular intento de acceso desde un sensor RFID
        Endpoint: POST /api/eventos/intentar_acceso/
        """
        serializer = AccesoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'error': True,
                'message': 'Error de validación',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        codigo_uid = serializer.validated_data['codigo_uid']
        barrera_id = serializer.validated_data['barrera_id']
        
        try:
            sensor = Sensor.objects.get(codigo_uid=codigo_uid)
            barrera = Barrera.objects.get(pk=barrera_id)
        except Sensor.DoesNotExist:
            # Sensor no encontrado - acceso denegado
            barrera = Barrera.objects.get(pk=barrera_id)
            evento = Evento.objects.create(
                barrera=barrera,
                tipo_acceso=Evento.DENEGADO,
                origen=Evento.AUTOMATICO,
                observaciones=f'Intento de acceso con código UID desconocido: {codigo_uid}'
            )
            return Response({
                'acceso': False,
                'mensaje': 'Acceso denegado - Sensor no registrado',
                'evento_id': evento.id
            }, status=status.HTTP_403_FORBIDDEN)
        
        except Barrera.DoesNotExist:
            return Response({
                'error': True,
                'message': 'Barrera no encontrada',
                'details': {'barrera_id': 'ID inválido'}
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validar estado del sensor
        if sensor.estado != Sensor.ACTIVO:
            evento = Evento.objects.create(
                sensor=sensor,
                barrera=barrera,
                tipo_acceso=Evento.DENEGADO,
                origen=Evento.AUTOMATICO,
                observaciones=f'Acceso denegado - Sensor en estado: {sensor.get_estado_display()}'
            )
            return Response({
                'acceso': False,
                'mensaje': f'Acceso denegado - Sensor {sensor.get_estado_display()}',
                'evento_id': evento.id
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Acceso permitido
        barrera.estado = Barrera.ABIERTA
        barrera.ultima_apertura = timezone.now()
        barrera.save()
        
        evento = Evento.objects.create(
            sensor=sensor,
            barrera=barrera,
            tipo_acceso=Evento.PERMITIDO,
            origen=Evento.AUTOMATICO,
            observaciones='Acceso permitido automáticamente'
        )
        
        return Response({
            'acceso': True,
            'mensaje': 'Acceso permitido',
            'sensor': sensor.nombre,
            'barrera': barrera.nombre,
            'evento_id': evento.id
        }, status=status.HTTP_200_OK)
