from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from reservations.models import Reservation
from .models import Resource, ResourceType


class ResourceTypeModelTest(APITestCase):
    def test_create_resource_type(self):
        rt = ResourceType.objects.create(
            name="Cancha", description="Cancha deportiva"
        )
        self.assertEqual(str(rt), "Cancha")
        self.assertEqual(rt.description, "Cancha deportiva")

    def test_resource_type_unique_name(self):
        ResourceType.objects.create(name="Cancha")
        with self.assertRaises(Exception):
            ResourceType.objects.create(name="Cancha")


class ResourceModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resource_type = ResourceType.objects.create(name="Salon")

    def test_create_active_resource(self):
        resource = Resource.objects.create(
            name="Salon Principal",
            resource_type=self.resource_type,
            is_active=True,
        )
        self.assertEqual(str(resource), "Salon Principal")
        self.assertTrue(resource.is_active)

    def test_create_inactive_resource(self):
        resource = Resource.objects.create(
            name="Salon Secundario",
            resource_type=self.resource_type,
            is_active=False,
        )
        self.assertFalse(resource.is_active)

    def test_resource_type_relation(self):
        resource = Resource.objects.create(
            name=" Sala A",
            resource_type=self.resource_type,
        )
        self.assertEqual(resource.resource_type.name, "Salon")

    def test_resource_type_on_delete_protect(self):
        Resource.objects.create(
            name="Sala A",
            resource_type=self.resource_type,
        )
        with self.assertRaises(Exception):
            self.resource_type.delete()


class ResourceAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create_user(
            username="admin", password="pass123", is_staff=True
        )
        cls.regular_user = User.objects.create_user(
            username="mateo", password="pass123"
        )
        cls.resource_type = ResourceType.objects.create(name="Cancha")
        Resource.objects.create(
            name="Cancha 1",
            resource_type=cls.resource_type,
            is_active=True,
        )
        Resource.objects.create(
            name="Cancha 2",
            resource_type=cls.resource_type,
            is_active=True,
        )
        Resource.objects.create(
            name="Cancha Inactiva",
            resource_type=cls.resource_type,
            is_active=False,
        )

    def setUp(self):
        self.client.force_authenticate(user=self.staff_user)

    def test_list_active_resources_only(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/resources/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [r["name"] for r in response.data]
        self.assertIn("Cancha 1", names)
        self.assertIn("Cancha 2", names)
        self.assertNotIn("Cancha Inactiva", names)

    def test_list_resource_types(self):
        response = self.client.get("/api/resource-types/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [rt["name"] for rt in response.data]
        self.assertIn("Cancha", names)

    def test_list_all_resources_with_todas(self):
        response = self.client.get("/api/resources/?todas=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [r["name"] for r in response.data]
        self.assertIn("Cancha 1", names)
        self.assertIn("Cancha 2", names)
        self.assertIn("Cancha Inactiva", names)

    def test_todas_without_auth_returns_active_only(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/resources/?todas=true")
        names = [r["name"] for r in response.data]
        self.assertNotIn("Cancha Inactiva", names)

    def test_create_resource_type(self):
        data = {"name": "Salon", "description": "Salon de eventos"}
        response = self.client.post("/api/resource-types/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ResourceType.objects.count(), 2)

    def test_create_resource_type_unauthenticated_returns_403(self):
        self.client.force_authenticate(user=None)
        data = {"name": "Salon", "description": "Salon de eventos"}
        response = self.client.post("/api/resource-types/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_cannot_create_resource_type(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {"name": "Salon"}
        response = self.client.post("/api/resource-types/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_resource_type_duplicate_returns_400(self):
        data = {"name": "Cancha"}
        response = self.client.post("/api/resource-types/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_resource_type_detail(self):
        response = self.client.get(
            f"/api/resource-types/{self.resource_type.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Cancha")

    def test_update_resource_type(self):
        response = self.client.patch(
            f"/api/resource-types/{self.resource_type.pk}/",
            {"description": "Cancha de futbol"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resource_type.refresh_from_db()
        self.assertEqual(self.resource_type.description, "Cancha de futbol")

    def test_delete_resource_type(self):
        rt = ResourceType.objects.create(name="Temporal")
        response = self.client.delete(f"/api/resource-types/{rt.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ResourceType.objects.count(), 1)

    def test_delete_resource_type_with_resources_returns_400(self):
        response = self.client.delete(
            f"/api/resource-types/{self.resource_type.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_resource(self):
        data = {
            "name": "Cancha 3",
            "resource_type": self.resource_type.pk,
        }
        response = self.client.post("/api/resources/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Resource.objects.count(), 4)

    def test_create_resource_unauthenticated_returns_403(self):
        self.client.force_authenticate(user=None)
        data = {
            "name": "Cancha 3",
            "resource_type": self.resource_type.pk,
        }
        response = self.client.post("/api/resources/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_cannot_create_resource(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {
            "name": "Cancha 3",
            "resource_type": self.resource_type.pk,
        }
        response = self.client.post("/api/resources/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_resource_missing_type_returns_400(self):
        data = {"name": "Cancha 3"}
        response = self.client.post("/api/resources/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_resource_detail(self):
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.get(f"/api/resources/{resource.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("resource_type_name", response.data)

    def test_update_resource(self):
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.patch(
            f"/api/resources/{resource.pk}/",
            {"name": "Cancha 1 Actualizada"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resource.refresh_from_db()
        self.assertEqual(resource.name, "Cancha 1 Actualizada")

    def test_toggle_resource_active(self):
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.patch(
            f"/api/resources/{resource.pk}/",
            {"is_active": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resource.refresh_from_db()
        self.assertFalse(resource.is_active)

    def test_delete_resource(self):
        resource = Resource.objects.create(
            name="Temporal", resource_type=self.resource_type
        )
        response = self.client.delete(f"/api/resources/{resource.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Resource.objects.count(), 3)

    def test_delete_resource_with_reservations_returns_400(self):
        resource = Resource.objects.filter(is_active=True).first()
        Reservation.objects.create(
            user=self.staff_user,
            resource=resource,
            start_datetime=datetime(2030, 6, 1, 10, 0),
            end_datetime=datetime(2030, 6, 1, 11, 0),
        )
        response = self.client.delete(
            f"/api/resources/{resource.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("reservas asociadas", response.data["detail"])

    def test_unauthenticated_detail_returns_200(self):
        self.client.force_authenticate(user=None)
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.get(f"/api/resources/{resource.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_patch_returns_403(self):
        self.client.force_authenticate(user=None)
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.patch(
            f"/api/resources/{resource.pk}/",
            {"name": "X"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_patch_returns_403(self):
        self.client.force_authenticate(user=self.regular_user)
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.patch(
            f"/api/resources/{resource.pk}/",
            {"name": "X"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_delete_returns_403(self):
        self.client.force_authenticate(user=None)
        resource = Resource.objects.filter(is_active=True).first()
        response = self.client.delete(f"/api/resources/{resource.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_delete_returns_403(self):
        self.client.force_authenticate(user=self.regular_user)
        resource = Resource.objects.create(
            name="Temporal", resource_type=self.resource_type
        )
        response = self.client.delete(f"/api/resources/{resource.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
