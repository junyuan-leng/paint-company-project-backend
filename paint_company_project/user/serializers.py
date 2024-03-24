from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField
from paint_company_project.user.models import User


class UserSerializer(serializers.ModelSerializer):
    id = HashidSerializerCharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_head_office_staff",
            "can_view_paint_list",
            "can_edit_paint_status",
            "can_edit_paint_inventory",
        ]