from rest_framework import serializers
from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        metric = self.context.get('metric')

        if metric:
            # Include the requested metric field in the serialized data
            representation[metric] = getattr(instance, metric)

        return representation
