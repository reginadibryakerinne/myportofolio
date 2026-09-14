from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from main.models import Experience, Skill


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
    