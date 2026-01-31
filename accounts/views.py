import re
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

import accounts.models as account_models
from . import serializers


def generate_tokens(user):
    tokens = RefreshToken.for_user(user)

    return {
        'access': str(tokens.access_token),
        'refresh': str(tokens)
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    email = request.data.get('email').strip()
    password = request.data.get('password').strip()

    try:
        user = account_models.CustomUser.objects.get(email__iexact=email)

        if user.check_password(password):
            token = generate_tokens(user)

            return Response({
                "status": True,
                "user": serializers.UserSerializers(user).data,
                "token": token
            }, status=status.HTTP_200_OK)

    except account_models.CustomUser.DoesNotExist:
        return Response({
            "status": False,
            "message": "Email and password does not match"
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        "status": False,
        "message": "Either Email and password does not match or not provided"
    }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def Register(request):
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,16}$'

    name = request.data.get('name').strip()
    email = request.data.get('email').strip()
    password = request.data.get('password').strip()
    date_of_birth = request.data.get('date_of_birth').strip()

    if not any([name, email, password, date_of_birth]):
        return Response({
            "status": False,
            "message": "Name, Email, Password, Date of Birth all are required"
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    if account_models.CustomUser.objects.filter(email=email).exists():
        return Response({
            "status": False,
            "message": "Email already exists"
        }, status=status.HTTP_409_CONFLICT)

    if not re.match(password_regex, password):
        return Response({
            "status": False,
            "message": "Password must be 8–16 characters long and include at least one uppercase letter, one number, and one special character."
        })

    date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()

    user = account_models.CustomUser(
        name=name,
        email=email,
        date_of_birth=date_of_birth
    )
    user.set_password(password)
    user.save()

    token = generate_tokens(user)

    return Response({
        "status": True,
        "user": serializers.UserSerializers(user).data,
        "token": token
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    try:
        refresh = request.data.get("refresh")

        if not refresh:
            return Response(
                {
                    "status": False,
                    "message": "Refresh token required"
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        token = RefreshToken(refresh)
        token.blacklist()

        return Response(
            {
                "status": True,
                "message": "Logged out successfully"
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {
                "status": False,
                "message": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST,
        )
