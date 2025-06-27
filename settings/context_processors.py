from django.urls import resolve

def breadcrumbs(request):
    path_parts = request.path.strip("/").split("/")
    breadcrumbs = []
    current_path = ""

    for part in path_parts:
        current_path += f"/{part}"
        breadcrumbs.append({"name": part.capitalize(), "url": current_path})

    return {"breadcrumbs": breadcrumbs}
