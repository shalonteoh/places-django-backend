from rest_framework import permissions

# Custom permission class


class IsAdminOrReadOnly(permissions.BasePermission):
    # Override
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class ViewMemberHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('countries.view_history')
