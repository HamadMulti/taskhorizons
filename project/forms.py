from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "block w-full p-2.5 text-sm border border-gray-300 rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                "placeholder": "Enter project title"
            }),
            "content": forms.Textarea(attrs={
                "class": "block w-full p-2.5 text-sm border border-gray-300 rounded-lg focus:ring-primary-600 focus:border-primary-600 dark:bg-gray-700 dark:border-gray-600 dark:text-white",
                "placeholder": "Write your project..."
            }),
        }
