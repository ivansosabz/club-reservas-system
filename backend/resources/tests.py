from rest_framework import status
from rest_framework.test import APITestCase
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
        cls.resource_type = ResourceType.objects.create(
            name="Salon"
        )

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
        cls.resource_type = ResourceType.objects.create(
            name="Cancha"
        )
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

    def test_list_active_resources_only(self):
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
