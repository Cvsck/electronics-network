from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Доступ разрешён только активным сотрудникам.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.user.is_active
        )
