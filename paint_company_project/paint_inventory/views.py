from django.db import transaction
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from paint_company_project.paint_inventory.models import Paint
from paint_company_project.paint_inventory.permissions import ViewPaintPermission, EditPaintInventoryPermission, EditPaintStatusPermission
from paint_company_project.paint_inventory.serializers import PaintSerializer, PaintInventoryUpdateSerializer, PaintStatusUpdateSerializer


class PaintViewSet(ModelViewSet):
    serializer_class = PaintSerializer
    
    def get_permissions(self):
        permission_classes = [ViewPaintPermission]
        if self.action == "status":
            permission_classes.append(EditPaintStatusPermission)
        elif self.action == "inventory":
            permission_classes.append(EditPaintInventoryPermission)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Paint.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "data": serializer.data,
            "total": len(serializer.data)
        }
        return Response(data)
    
    @action(detail=True, methods=["put"])
    def status(self, request, *args, **kwargs):
        paint_id = self.kwargs.get("pk")
        serializer = PaintStatusUpdateSerializer(data=request.data)
        if paint_id and serializer.is_valid():
            status = serializer.validated_data["status"]
            with transaction.atomic():
                paint = Paint.objects.get(id=paint_id)
                paint.status = status
                paint.save(update_fields=["status"])
            return Response(status=http_status.HTTP_200_OK, data=PaintSerializer(instance=paint).data)
        else:
            return Response(status=http_status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["put"])
    def inventory(self, request, *args, **kwargs):
        paint_id = self.kwargs.get("pk")
        serializer = PaintInventoryUpdateSerializer(data=request.data)
        if paint_id and serializer.is_valid():
            inventory = serializer.validated_data["inventory"]
            with transaction.atomic():
                paint = Paint.objects.get(id=paint_id)
                paint.inventory = inventory
                paint.save(update_fields=["inventory"])
            return Response(status=http_status.HTTP_200_OK, data=PaintSerializer(instance=paint).data)
        else:
            return Response(status=http_status.HTTP_400_BAD_REQUEST)
