from rest_framework.permissions import BasePermission


class ViewPaintPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_head_office_staff or request.user.can_view_paint_list:
            return True
        else:
            return False


class EditPaintInventoryPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.can_edit_paint_inventory:
            return True
        else:
            return False
    

class EditPaintStatusPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_head_office_staff or request.user.can_edit_paint_status:
            return True
        else:
            return False