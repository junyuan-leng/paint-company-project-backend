from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from paint_company_project.user.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = [
        "id",
        "is_head_office_staff",
        "can_view_paint_list",
        "can_edit_paint_status",
        "can_edit_paint_inventory",
        "username",
        "password",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_head_office_staff",
                    "can_view_paint_list",
                    "can_edit_paint_status",
                    "can_edit_paint_inventory",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
