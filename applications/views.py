from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application
from applications.serializers import ApplicationSerializer
from users.models import User


# Create your views here.


class ApplicationsView(APIView):

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')

        user = request.user

        if not title or title.strip() == "":
            return Response({'error': 'Please provide a valid title'}, status=status.HTTP_400_BAD_REQUEST)

        if not description or description.strip() == "":
            return Response({'error': 'Please provide a valid description'}, status=status.HTTP_400_BAD_REQUEST)

        Application.objects.create(
            title=title,
            description=description,
            creator=user
        )

        return Response({'message': 'New application created successfully',
                         },
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user

        application_qs = Application.objects.filter(creator=user)

        serializer = ApplicationSerializer(application_qs, many=True)

        data = {'applications': serializer.data}

        return Response({'message': "Request successful",
                         'data': data
                         }, status=status.HTTP_200_OK)


class ApplicationView(APIView):

    def get(self, request, application_id):
        user = request.user

        application = Application.objects.get(creator=user, id=application_id)

        serializer = ApplicationSerializer(application)

        data = {'application': serializer.data}

        return Response({'message': "Application deleted successfully",
                         "data": data
                         }, status=status.HTTP_200_OK)

    def delete(self, request, application_id):
        user = request.user

        Application.objects.filter(creator=user, id=application_id).delete()

        return Response({'message': "Application deleted successfully",

                         }, status=status.HTTP_200_OK)

    def patch(self, request, application_id):
        title = request.data.get('title')
        description = request.data.get('description')

        user = request.user

        Application.objects.filter(creator=user, id=application_id).update(
            title=title,
            description=description
        )

        return Response({'message': "Application updated successfully",

                         }, status=status.HTTP_200_OK)
