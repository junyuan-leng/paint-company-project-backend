from django.contrib import admin
from paint_company_project.paint_inventory.models import Paint


@admin.register(Paint)
class PaintAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "color",
        "status", 
        "inventory"
    ]
