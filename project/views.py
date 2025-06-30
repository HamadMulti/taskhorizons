from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

@login_required
def projects_list(request):
    """List all projects for the user."""
    projects = Project.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "projects/project_list.html", {"projects": projects})

@login_required
def add_project(request):
    """Create a new project."""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect("projects:project_list")
    else:
        form = ProjectForm()
    
    return render(request, "projects/project_form.html", {"form": form})

@login_required
def edit_project(request, project_id):
    """Edit an existing project."""
    project = get_object_or_404(project, id=project_id, user=request.user)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:project_list")
    else:
        form = ProjectForm(instance=project)
    
    return render(request, "projects/project_form.html", {"form": form})

@login_required
def delete_project(request, project_id):
    """Delete a project."""
    project = get_object_or_404(project, id=project_id, user=request.user)
    if request.method == "POST":
        project.delete()
        return redirect("projects:project_list")
    
    return render(request, "projects/project_confirm_delete.html", {"project": project})
