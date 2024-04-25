from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from hxnterapiapi.models import Mission, Hunter, Wanted


class MissionViewSet(viewsets.ViewSet):
    """Mission view set"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized instance
        """

        mission = Mission()
        mission.hunter_id = request.data["hunter"]
        mission.title = request.data["title"]
        mission.description = request.data["description"]
        mission.wanted_id = request.data["wanted"]
        mission.type = request.data["type"]

        try:
            mission.save()
            serializer = MissionSerializer(mission)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single mission
        Returns:
            Response -- JSON serialized instance
        """
        try:
            mission = Mission.objects.get(pk=pk)
            serializer = MissionSerializer(mission)
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
            mission.hunter_id = request.data["hunter"]
            mission.title = request.data["title"]
            mission.description = request.data["description"]
            mission.wanted_id = request.data["wanted"]
            mission.type = request.data["type"]
            mission.save()
        except Mission.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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


class MissionSerializer(serializers.ModelSerializer):
    """JSON serializer for missions"""

    class Meta:
        model = Mission
        fields = ("id", "hunter", "title", "description", "wanted", "type")
