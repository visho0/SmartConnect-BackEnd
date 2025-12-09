from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, Departamento, Sensor, Barrera, Evento

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'rol', 
                  'first_name', 'last_name', 'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        usuario = Usuario.objects.create(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'first_name', 'last_name']

class DepartamentoSerializer(serializers.ModelSerializer):
    sensores_count = serializers.SerializerMethodField()
    barreras_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'sensores_count', 'barreras_count',
                  'fecha_creacion', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']
    
    def get_sensores_count(self, obj):
        return obj.sensores.count()
    
    def get_barreras_count(self, obj):
        return obj.barreras.count()

class SensorSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'codigo_uid', 'nombre', 'estado', 'departamento', 
                  'departamento_nombre', 'usuario', 'usuario_username',
                  'fecha_registro', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_registro', 'fecha_actualizacion']
    
    def validate_codigo_uid(self, value):
        # Validar unicidad del código UID
        if self.instance:
            if Sensor.objects.filter(codigo_uid=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Este código UID/MAC ya está registrado.")
        else:
            if Sensor.objects.filter(codigo_uid=value).exists():
                raise serializers.ValidationError("Este código UID/MAC ya está registrado.")
        return value

class BarreraSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Barrera
        fields = ['id', 'nombre', 'estado', 'departamento', 'departamento_nombre',
                  'fecha_creacion', 'fecha_actualizacion', 'ultima_apertura']
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion', 'ultima_apertura']

class EventoSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    sensor_codigo = serializers.CharField(source='sensor.codigo_uid', read_only=True)
    barrera_nombre = serializers.CharField(source='barrera.nombre', read_only=True)
    usuario_operador_username = serializers.CharField(source='usuario_operador.username', read_only=True)
    
    class Meta:
        model = Evento
        fields = ['id', 'sensor', 'sensor_nombre', 'sensor_codigo', 'barrera', 'barrera_nombre',
                  'tipo_acceso', 'origen', 'usuario_operador', 'usuario_operador_username',
                  'observaciones', 'fecha_evento']
        read_only_fields = ['id', 'fecha_evento']

class AccesoSerializer(serializers.Serializer):
    """Serializer para validar intentos de acceso desde sensores"""
    codigo_uid = serializers.CharField(max_length=50, required=True)
    barrera_id = serializers.IntegerField(required=True)

