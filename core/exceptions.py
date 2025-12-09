from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError

def custom_exception_handler(exc, context):
    """
    Manejo personalizado de excepciones para devolver respuestas JSON consistentes
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'Ha ocurrido un error',
            'details': {}
        }
        
        if response.status_code == 400:
            custom_response_data['message'] = 'Error de validación'
            custom_response_data['details'] = response.data
        
        elif response.status_code == 401:
            custom_response_data['message'] = 'No autenticado. Se requiere token JWT válido'
            custom_response_data['details'] = {'authentication': 'Token requerido o inválido'}
        
        elif response.status_code == 403:
            custom_response_data['message'] = 'No tiene permisos para realizar esta acción'
            custom_response_data['details'] = {'permission': 'Acceso denegado'}
        
        elif response.status_code == 404:
            if isinstance(exc, Http404):
                custom_response_data['message'] = 'Recurso no encontrado'
            else:
                custom_response_data['message'] = 'Objeto no encontrado'
            custom_response_data['details'] = {'not_found': str(exc)}
        
        response.data = custom_response_data
    
    else:
        # Manejar excepciones no capturadas por DRF
        if isinstance(exc, DjangoValidationError):
            response = Response({
                'error': True,
                'message': 'Error de validación',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return response

