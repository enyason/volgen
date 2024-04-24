from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application, Submission
from applications.serializers import ApplicationSerializer, SubmissionSerializer
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
    permission_classes = [AllowAny]

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


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_application_view(request, application_id):
#     application = Application.objects.get(id=application_id)
#
#     serializer = ApplicationSerializer(application)
#
#     data = {'application': serializer.data}
#
#     return Response({'message': "Application deleted successfully",
#                      "data": data
#                      }, status=status.HTTP_200_OK)


class SubmissionsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, application_id):

        files: [InMemoryUploadedFile] = request.FILES.values()

        full_name = request.data.get('full_name')
        email = request.data.get('email')
        gender = request.data.get('gender')
        country = request.data.get('country')
        cover_letter = request.data.get('cover_letter')
        resume = "https://emmanuelenya.netlify.app/assets/files/resume.pdf"

        if not full_name or full_name.strip() == "":
            return Response({'error': 'Please provide a valid name'}, status=status.HTTP_400_BAD_REQUEST)

        if not gender or gender.strip() == "":
            return Response({'error': 'Please provide a valid gender'}, status=status.HTTP_400_BAD_REQUEST)

        if not country or country.strip() == "":
            return Response({'error': 'Please provide a valid country'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Please provide a valid email'}, status=status.HTTP_400_BAD_REQUEST)

        Submission.objects.create(
            application_id=application_id,
            full_name=full_name,
            email=email,
            gender=gender,
            country=country,
            cover_letter=cover_letter,
            resume=resume
        )

        return Response({'message': 'Submission was successfully',
                         },
                        status=status.HTTP_200_OK)

    def get(self, request, application_id):
        user = request.user

        application = Application.objects.get(id=application_id, creator=user)

        submission_qs = Submission.objects.filter(application=application)

        serializer = SubmissionSerializer(submission_qs, many=True)

        data = {'submissions': serializer.data}

        return Response({'message': "Request successful",
                         'data': data
                         }, status=status.HTTP_200_OK)
