from rest_framework import permissions

class PermissionName(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        perms = user.get_all_permissions()
        return True
    
class UpdateAndDestroyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
             return True
        if request.user.id == obj.posted_by.id:
            return True
            
        return False