from django.urls import path

from applications.views import ApplicationsView, ApplicationView, SubmissionsView

urlpatterns = [
    path('applications', ApplicationsView.as_view()),
    path('applications/<application_id>', ApplicationView.as_view()),
    path('applications/<application_id>/submissions', SubmissionsView.as_view()),
]
