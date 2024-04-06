from django.urls import path

from applications.views import ApplicationsView, ApplicationView

urlpatterns = [
    path('applications', ApplicationsView.as_view()),
    path('applications/<application_id>', ApplicationView.as_view()),
]
