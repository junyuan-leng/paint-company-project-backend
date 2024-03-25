from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from paint_company_project.paint_inventory.models import Paint


class PaintSerializer(serializers.ModelSerializer):
    # defines what data we shall return in the paint list response
    id = HashidSerializerCharField(read_only=True)
    class Meta:
        model = Paint
        fields = [
            "id",
            "color",
            "status",
            "inventory",
        ]


class PaintStatusUpdateSerializer(serializers.ModelSerializer):
    # verifies paint status update request payload
    class Meta:
        model = Paint
        fields = [
            "status",
        ]


class PaintInventoryUpdateSerializer(serializers.ModelSerializer):
    # verifies paint inventory update request payload
    class Meta:
        model = Paint
        fields = [
            "inventory",
        ]