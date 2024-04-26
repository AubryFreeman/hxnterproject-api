from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import serializers, status, viewsets
from hxnterapiapi.models import Mission, Hunter, Wanted, Type


class MissionViewSet(viewsets.ViewSet):
    """Mission view set"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized instance
        """
        user = request.user
        hunter, created = Hunter.objects.get_or_create(user=user)

        mission = Mission.objects.create(
            hunter=hunter,
            title=request.data["title"],
            description=request.data["description"],
            wanted_id=request.data["wanted"],
            type_id=request.data["type"],
        )

        serializer = MissionSerializer(mission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single mission
        Returns:
            Response -- JSON serialized instance
        """
        try:
            mission = Mission.objects.get(pk=pk)
            serializer = MissionSerializer(
                mission,
            )
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """Handle GET request for all missions
        Returns:
            Response -- JSON serialized list of missions
        """
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests
        Returns:
            Response -- Empty body with 204 status code
        """

        try:
            mission = Mission.objects.get(pk=pk)
            mission.hunter_id = request.auth.user_id
            mission.title = request.data["title"]
            mission.description = request.data["description"]
            mission.wanted_id = request.data["wanted"]
            mission.type_id = request.data["type"]
            mission.save()
        except Mission.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        return Response(None, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single mission
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            mission = Mission.objects.get(pk=pk)
            mission.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Mission.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for missions"""

    class Meta:
        model = Type
        fields = ("id", "name")


class HunterSerializer(serializers.ModelSerializer):
    """JSON serializer for missions"""

    name = serializers.SerializerMethodField()

    class Meta:
        model = Hunter
        fields = ("user_id", "name")

    def get_name(self, obj):
        user = User.objects.get(pk=obj.user_id)
        return f"{user.first_name} {user.last_name}"


class MissionSerializer(serializers.ModelSerializer):
    """JSON serializer for missions"""

    token = serializers.SerializerMethodField()
    type = TypeSerializer()
    hunter = HunterSerializer()
    hunter_name = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = (
            "id",
            "hunter_name",
            "hunter",
            "title",
            "description",
            "wanted_id",
            "type",
            "token",
        )

    def get_token(self, obj):
        hunter = User.objects.get(pk=obj.hunter.user_id)
        return Token.objects.get(user=hunter).key

    def get_hunter_name(self, obj):
        user = User.objects.get(pk=obj.hunter.user_id)
        return f"{user.first_name} {user.last_name}"
