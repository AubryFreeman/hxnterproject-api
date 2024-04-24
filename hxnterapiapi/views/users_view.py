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


class Users(ViewSet):
    # Other methods...
    @csrf_exempt
    @action(detail=False, methods=["post"])
    def login_user(self, request):
        """Handles the authentication of a user"""

        body = request.body.decode("utf-8")
        req_body = json.loads(body)

        if request.method == "POST":
            name = req_body["username"]
            pass_word = req_body["password"]
            authenticated_user = authenticate(username=name, password=pass_word)

            if authenticated_user is not None:
                token, _ = Token.objects.get_or_create(user=authenticated_user)
                data = {"valid": True, "token": token.key, "id": authenticated_user.id}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"valid": False}
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        return Response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
