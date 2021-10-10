from django.urls import path
from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    path("", views.list_peak),
    path("int:pk>", views.detail_peak),
    path("insert_with_csv", views.upload_list_peak),
    path('docs/', include_docs_urls(title='Peak API'))
]
