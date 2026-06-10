from django.urls import path

from .views import (
    resource_detail,
    resource_list_create,
    resource_type_detail,
    resource_type_list_create,
)

urlpatterns = [
    path("resource-types/", resource_type_list_create, name="resource-type-list-create"),
    path("resource-types/<int:pk>/", resource_type_detail, name="resource-type-detail"),
    path("resources/", resource_list_create, name="resource-list-create"),
    path("resources/<int:pk>/", resource_detail, name="resource-detail"),
]
