from rest_framework.permissions import BasePermission


class ViewPaintPermission(BasePermission):
    # users with ViewPaintPermission can view the paint list
    def has_permission(self, request, view):
        if request.user.is_head_office_staff or request.user.can_view_paint_list:
            return True
        else:
            return False


class EditPaintInventoryPermission(BasePermission):
    # users with EditPaintInventoryPermission can update/edit paint inventory
    def has_permission(self, request, view):
        if request.user.can_edit_paint_inventory:
            return True
        else:
            return False
    

class EditPaintStatusPermission(BasePermission):
    # users with EditPaintStatusPermission can update/edit paint status
    def has_permission(self, request, view):
        if request.user.is_head_office_staff or request.user.can_edit_paint_status:
            return True
        else:
            return False