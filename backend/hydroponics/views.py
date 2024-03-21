from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from hydroponics.models import HydroponicSystem, Measurement
from hydroponics.serializers import (
    HydroponicSystemSerializer,
    MeasurementCreateSerializer,
    MeasurementDetailSerializer,
)


class HydroponicSystemView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HydroponicSystemSerializer
    queryset = HydroponicSystem.objects.all()

    def get_queryset(self):
        user = self.request.user.pk
        return self.queryset.filter(owner__pk=user)

    def get_object(self):
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(HydroponicSystem, pk=pk)
        user = self.request.user
        if obj.owner != user:
            raise PermissionDenied(
                {
                    "message": "You are not allowed to perform operations on this object"
                },
                code=status.HTTP_403_FORBIDDEN,
            )

        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        LIMIT = 10
        measurements = instance.measurements.order_by("-when_measured")[:LIMIT]
        measurement_serializer = MeasurementDetailSerializer(
            measurements, many=True
        )
        my_serializer = self.get_serializer(instance)

        data = {
            "details": my_serializer.data,
            "measurements": measurement_serializer.data,
        }

        return Response(data)


class MeasurementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, hydroponics_id: int, format=None):
        if not is_owner_of_system(request, hydroponics_id):
            raise PermissionDenied(
                {
                    "message": "You are not allowed to perform operations on this object"
                },
                code=status.HTTP_403_FORBIDDEN,
            )

        LIMIT = 10
        measurements = Measurement.objects.filter(
            hydroponic_system__pk=hydroponics_id
        ).order_by("-when_measured")[:LIMIT]

        serializer = MeasurementDetailSerializer(measurements, many=True)
        return JsonResponse({"measurements": serializer.data})

    def post(self, request: Request, hydroponics_id: int, format=None):
        if not is_owner_of_system(request, hydroponics_id):
            raise PermissionDenied(
                {
                    "message": "You are not allowed to perform operations on this object"
                },
                code=status.HTTP_403_FORBIDDEN,
            )

        hydroponics = get_object_or_404(HydroponicSystem, pk=hydroponics_id)

        serializer = MeasurementCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(hydroponic_system=hydroponics)
            return Response(
                {"measurement": serializer.data}, status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


def is_owner_of_system(request, hydroponics_id: int) -> bool:
    hydroponics = get_object_or_404(HydroponicSystem, pk=hydroponics_id)
    return hydroponics.owner == request.user
