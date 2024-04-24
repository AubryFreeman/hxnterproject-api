import json
from django.http import HttpResponseServerError, HttpResponse, HttpResponseNotAllowed
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializers
    """

    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(view_name="user", lookup_field="id")
        fields = (
            "id",
            "url",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "date_joined",
        )


class Users(ViewSet):
    """Users for Hxnter
    Purpose: Allow a user to communicate with the Hxnter database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
    """

    @action(detail=False, methods=["post"], url_path="login")
    def login_user(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get_or_create(user=authenticated_user)[0]

            serializer = UserSerializer(
                authenticated_user, context={"request": request}
            )
            data = {"valid": True, "token": token.key, "user": serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Purpose: Allow a user to communicate with the Hxnter database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)
