from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from task.models import Task
from project.models import Project

@login_required
def dashboard(request):
    """
    Displays an overview of the user's tasks, focus sessions, habits, and reports.
    """
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    tasks = Task.objects.filter(user=request.user, status__in=["pending", "in_progress"]).order_by("due_date")[:5]
    projects = Project.objects.filter(user=request.user).order_by("-created_at")[:5]

    return render(request, "dashboard/index.html", {
        "tasks": tasks,
        "projects": projects,
        "today": today,
        "start_of_week": start_of_week,
        "end_of_week": end_of_week,
    })
