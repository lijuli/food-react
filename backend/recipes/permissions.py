from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    def is_author_or_admin(self, request, obj):
        return (request.user == obj.author
                or request.user.is_staff
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.method in ('DELETE', 'PATCH', 'POST')
                    and self.is_author_or_admin(request, obj)
                    and request.user.is_authenticated)
                )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser
