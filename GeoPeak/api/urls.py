from django.urls import path
from rest_framework.documentation import include_docs_urls

from . import views

urlpatterns = [
    path("peak", views.list_peak),
    path("peak/<int:pk>", views.detail_peak),
    path("upload_list_peak", views.upload_list_peak),
    path('docs/', include_docs_urls(title='Peak API'))
]
