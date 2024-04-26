from rest_framework import viewsets
from hxnterapiapi.models import Type
from rest_framework import serializers
from rest_framework.response import Response


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class TypeViewSet(viewsets.ViewSet):
    def list(self, request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data)
