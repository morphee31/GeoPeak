from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from .views import ListPeakViews, DetailPeakViews

from . import views

schema_view = get_schema_view(title="Example API")

urlpatterns = [
    path("", ListPeakViews.as_view()),
    path("<int:pk>", DetailPeakViews.as_view()),
    path("put_with_csv", views.upload_list_peak),
    path('docs/', include_docs_urls(title='Peak API'))

]
