from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from paint_company_project.user.serializers import UserSerializer


User = get_user_model()

class UserViewSet(GenericViewSet):
    
    @action(detail=False, methods=["get"])
    def me(self, request):
        user_id = request.user.id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
