import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project, Experience, Skill


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="testpassword123",
        )

        self.regular_user = User.objects.create_user(
            username="regular",
            password="testpassword123",
        )

        self.editor_group = Group.objects.create(name="Editor")

        self.editor = User.objects.create_user(
            username="editor",
            password="testpassword123",
        )
        self.editor.groups.add(self.editor_group)

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami Django.",
            category="part-time",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )
        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

        self.valid_payload = {
            "title": "Web Developer",
            "description": "Mengembangkan aplikasi web.",
            "category": "part-time",
        }

    def test_get_experience_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            self.experience.title,
        )

    def test_get_experience_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["title"],
            self.experience.title,
        )

    def test_search_experience_by_title(self):
        response = self.client.get(
            self.list_url,
            {"title": "Asisten Dosen"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_experience_returns_empty(self):
        response = self.client.get(
            self.list_url,
            {"title": "Pengalaman Tidak Ada"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_nonexistent_experience(self):
        url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_cannot_create_experience(self):
        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_visitor_cannot_update_experience(self):
        response = self.client.patch(
            self.detail_url,
            {"description": "Deskripsi baru."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description,
            "Membantu mahasiswa memahami Django.",
        )

    def test_visitor_cannot_delete_experience(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_owner_can_create_experience(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)

    def test_owner_can_update_experience(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"description": "Deskripsi diperbarui."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description,
            "Deskripsi diperbarui.",
        )

    def test_owner_can_delete_experience(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_regular_user_cannot_create_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_regular_user_cannot_update_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.patch(
            self.detail_url,
            {"description": "Deskripsi baru."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description,
            "Membantu mahasiswa memahami Django.",
        )

    def test_regular_user_cannot_delete_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_editor_can_update_experience(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"description": "Diperbarui oleh Editor."},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.description,
            "Diperbarui oleh Editor.",
        )

    def test_editor_cannot_create_experience(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_cannot_delete_experience(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Experience.objects.filter(pk=self.experience.pk).exists()
        )

    def test_create_experience_with_empty_title(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.valid_payload,
            "title": "   ",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)

    def test_create_experience_with_empty_description(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.valid_payload,
            "description": "   ",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)

    def test_user_can_star_experience(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.experience.starred_by.filter(
                pk=self.regular_user.pk
            ).exists()
        )

    def test_user_can_unstar_experience(self):
        self.experience.starred_by.add(self.regular_user)
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.experience.starred_by.filter(
                pk=self.regular_user.pk
            ).exists()
        )

    def test_visitor_cannot_star_experience(self):
        response = self.client.post(self.star_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_csrf_protection_without_token(self):
        csrf_client = APIClient(enforce_csrf_checks=True)

        csrf_client.login(
            username="owner",
            password="testpassword123",
        )

        response = csrf_client.post(
            self.list_url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

class SkillAPITest(APITestCase):
    def setUp(self):
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(editor_group)
        self.regular = User.objects.create_user(username="regular", password="test-password")
        self.skill = Skill.objects.create(
            title="Django Development", description="Backend web", category="hard",
        )
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.star_url = reverse("api:skill-star", args=[self.skill.id])
        self.payload = {
            "title": "Teamwork", "description": "Collaboration skill",
            "category": "soft", "thumbnail": "https://example.com/icon.png",
        }

    def as_user(self, user=None):
        client = APIClient()
        if user is not None:
            client.force_authenticate(user)
        return client

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.skill.id))
        self.assertEqual(response.data[0]["category_display"], "Hard Skill")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        found = self.client.get(self.list_url, {"title": "DJANGO"})
        self.assertEqual(len(found.data), 1)
        empty = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(empty.status_code, status.HTTP_200_OK)
        self.assertEqual(empty.data, [])

    def test_missing_skill(self):
        url = reverse("api:skill-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_and_regular_cannot_write(self):
        for user in (None, self.regular):
            client = self.as_user(user)
            self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(client.patch(self.detail_url, {"title": "X"}, format="json").status_code, 403)
            self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Skill.objects.count(), 1)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Django Development")

    def test_editor_can_update_but_not_create_or_delete(self):
        client = self.as_user(self.editor)
        self.assertEqual(client.patch(self.detail_url, {"title": "Diubah"}, format="json").status_code, 200)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Teamwork")
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Skill.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        client = self.as_user(self.owner)
        created = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)
        patched = client.patch(self.detail_url, {"title": "Python"}, format="json")
        self.assertEqual(patched.status_code, status.HTTP_200_OK)
        self.assertEqual(patched.data["title"], "Python")
        self.assertEqual(client.delete(self.detail_url).status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Skill.objects.count(), 1)

    def test_invalid_input_returns_400_and_is_not_saved(self):
        client = self.as_user(self.owner)
        cases = {
            "title": {**self.payload, "title": "   "},
            "title ": {**self.payload, "title": "<img src=x onerror=alert(1)>"},
            "description": {**self.payload, "description": "<b></b>"},
            "category": {**self.payload, "category": "bukan-kategori"},
            "thumbnail": {**self.payload, "thumbnail": "javascript:alert(1)"},
        }
        for field, data in cases.items():
            with self.subTest(field=field):
                response = client.post(self.list_url, data, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field.strip(), response.data)
        self.assertEqual(Skill.objects.count(), 1)

    def test_computed_fields_are_read_only(self):
        client = self.as_user(self.owner)
        response = client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "category_display": "forged",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], [])
        self.assertEqual(response.data["category_display"], "Soft Skill")

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.as_user().post(self.star_url).status_code, 403)
        client = self.as_user(self.regular)
        first = client.post(self.star_url)
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertTrue(first.data["is_starred"])
        self.assertEqual(first.data["star_count"], 1)
        self.assertEqual(first.data["starred_by_names"], ["regular"])
        second = client.post(self.star_url)
        self.assertFalse(second.data["is_starred"])
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_wrong_method(self):
        client = self.as_user(self.owner)
        self.assertEqual(client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        client.get(self.list_url, HTTP_ACCEPT="text/html")      # Browsable API menyetel cookie CSRF
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Skill.objects.count(), 2)