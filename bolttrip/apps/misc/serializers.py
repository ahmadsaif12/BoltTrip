from rest_framework import serializers


class APIHealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    app = serializers.CharField()


class APIModuleSerializer(serializers.Serializer):
    name = serializers.CharField()
    path = serializers.CharField()
