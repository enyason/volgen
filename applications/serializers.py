from rest_framework.serializers import ModelSerializer

from applications.models import Application, Submission


class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class ApplicationSerializer(ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'title', 'description', 'date_created', 'date_modified', 'submissions']
