from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    count = serializers.IntegerField()
