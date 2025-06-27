from django.shortcuts import redirect, render

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
    return render(request, 'landing/home.html')
