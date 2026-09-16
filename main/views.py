from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Skill, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Regina Dibrya Kerinne Purba",
        "npm": "2506657296",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "An undergraduate with four years of experience in the creative field, actively developing expertise in visual communication, graphic design, and video editing." 
            "Work is carried out with a strong emphasis on aesthetics and precision, ensuring that every detail supports a cohesive and refined visual outcome. "
            "The primary focus is to deliver a superior visual experience, where high aesthetic standards meet the effective synchronization of information."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Regina Dibrya Kerinne Purba",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = {
        "name": "Regina Dibrya Kerinne Purba",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

...
def show_projects(request):
    context = {
        "name": "Burhan",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Regina Dibrya Kerinne Purba",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Regina Dibrya Kerinne Purba",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")