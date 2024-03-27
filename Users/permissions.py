from rest_framework import permissions

class UpdateAndDestroyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
       
        if request.method == "GET":
             return True
        if request.user.id == obj.id:
            return True
            
        return False