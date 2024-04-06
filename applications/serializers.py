from rest_framework.serializers import ModelSerializer

from applications.models import Application


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'title', 'description', 'date_created', 'date_modified']
