from django.forms import ModelForm, TextInput, Textarea, URLInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from main.models import Project, Experience, Skill

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()    

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori Pengalaman",
            "thumbnail": "Logo Lembaga Pengalaman",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Pengalaman",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "internship, research, volunteer, part-time, full-time, freelance",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]

        labels = {
            "title": "Skill",
            "description": "Deskripsi Skill",
            "category": "Kategori Skill",
            "thumbnail": "URL Skill",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Nama Skill",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsikan skillmu",
                    "rows": 3,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "hard, soft",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }