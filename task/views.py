from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    """Display all tasks for the logged-in user."""
    tasks = Task.objects.filter(user=request.user).order_by("due_date")
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_detail(request, task_id):
    """View details of a specific task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, "tasks/task_detail.html", {"task": task})

@login_required
def task_create(request):
    """Create a new task."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks:task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})

@login_required
def task_update(request, task_id):
    """Update an existing task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "task": task})

@login_required
def task_delete(request, task_id):
    """Delete a task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks:task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})
