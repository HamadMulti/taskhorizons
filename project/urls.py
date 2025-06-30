from django.urls import path
from .views import projects_list, add_project, edit_project, delete_project

app_name = "project"

urlpatterns = [
    path("", projects_list, name="project_list"),
    path("add/", add_project, name="add_project"),
    path("edit/<int:project_id>/", edit_project, name="edit_project"),
    path("delete/<int:project_id>/", delete_project, name="delete_project"),
]
