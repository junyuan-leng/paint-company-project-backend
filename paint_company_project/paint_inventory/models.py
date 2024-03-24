from django.db import models
from paint_company_project.paint_inventory.utils import CustomBigHashidAutoField


class Paint(models.Model):
    # paint color
    BLUE = "blue"
    GREY = "grey"
    BLACK = "black"
    WHITE = "white"
    PURPLE = "purple"
    PAINT_COLOR_CHOICES = (
        (BLUE, "Blue"),
        (GREY, "Grey"),
        (BLACK, "Black"),
        (WHITE, "White"),
        (PURPLE, "Purple"),
    )
    # paint status
    AVAILABLE = "available"
    RUNNING_LOW = "running_low"
    OUT_OF_STOCK = "out_of_stock"
    PAINT_STATUS_CHOICES = (
        (AVAILABLE, "Available"),
        (RUNNING_LOW, "Running Low"),
        (OUT_OF_STOCK, "Out of Stock"),
    )
    id = CustomBigHashidAutoField(primary_key=True, prefix="pnt_")
    color = models.CharField(max_length=255, choices=PAINT_COLOR_CHOICES, unique=True)
    status = models.CharField(max_length=255, choices=PAINT_STATUS_CHOICES)
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.color} paint"
