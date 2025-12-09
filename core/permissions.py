from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado:
    - Admin: CRUD completo
    - Operador: Solo lectura (GET)
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        return request.user.is_authenticated and request.user.rol == 'admin'

class IsAdmin(permissions.BasePermission):
    """
    Solo usuarios administradores pueden acceder
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'

