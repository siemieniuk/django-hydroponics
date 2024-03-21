from rest_framework import serializers

from hydroponics.models import HydroponicSystem, Measurement


class HydroponicSystemSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = HydroponicSystem
        fields = (
            "id",
            "name",
            "description",
            "created",
            "updated",
        )


class MeasurementCreateSerializer(serializers.ModelSerializer):
    hydroponic_system = serializers.PrimaryKeyRelatedField(
        queryset=HydroponicSystem.objects.all(),
        required=False,
        write_only=True,
    )
    when_measured = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Measurement
        fields = (
            "hydroponic_system",
            "water_ph",
            "water_tds",
            "water_temp",
            "when_measured",
        )


class MeasurementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ("when_measured", "water_ph", "water_tds", "water_temp")
