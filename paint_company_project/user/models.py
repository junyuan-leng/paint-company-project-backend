from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from paint_company_project.paint_inventory.utils import CustomBigHashidAutoField

class User(AbstractUser):
    id = CustomBigHashidAutoField(primary_key=True, prefix="usr_")
    is_head_office_staff = models.BooleanField(
        _("Permission to View KanBan"),
        default=False,
        help_text=_("Designates whether the user can view kanban."),
    )
    can_view_paint_list = models.BooleanField(
        _("Permission to View Paint List"),
        default=False,
        help_text=_("Designates whether the user can view paint list."),
    )
    can_edit_paint_status = models.BooleanField(
        _("Permission to Edit Paint Status"),
        default=False,
        help_text=_("Designates whether the user can edit paint status."),
    )
    can_edit_paint_inventory = models.BooleanField(
        _("Permission to Edit Paint Inventory"),
        default=False,
        help_text=_("Designates whether the user can edit paint inventory."),
    )