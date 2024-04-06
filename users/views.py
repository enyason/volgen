from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


# Create your views here.


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not email or not password:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(email=email)
            return Response({'error': 'email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email, password=password, first_name=first_name,
                                            last_name=last_name, is_active=True)

            token = Token.objects.create(user=user)

            data = {'access_token': token.key}

            return Response({'message': 'User created successfully',
                             'data': data
                             },
                            status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        data = {'access_token': token.key,
                'profile': get_user_profile(user)}

        return Response({'message': "Login successful",
                         'data': data
                         }, status=status.HTTP_200_OK)


def get_user_profile(user: User):
    return {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
