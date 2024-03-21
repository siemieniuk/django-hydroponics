from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from tokens.serializers import UserRegisterSerializer


@api_view(["POST"])
def user_registration_view(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        new_account = serializer.save()

        data = dict()
        data["response"] = "Your account has successfully been created"
        data["username"] = new_account.username
        data["email"] = new_account.email

        refresh = RefreshToken.for_user(new_account)
        data["token"] = {
            "refresh": f"{refresh}",
            "access": f"{refresh.access_token}",
        }

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
