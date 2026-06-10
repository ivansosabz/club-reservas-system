from datetime import date, time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase
from resources.models import Resource, ResourceType
from .models import Reservation


class ReservationModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        cls.resource_type = ResourceType.objects.create(
            name="Cancha", description="Cancha de tenis"
        )
        cls.resource = Resource.objects.create(
            name="Cancha 1",
            resource_type=cls.resource_type,
            is_active=True,
        )
        cls.inactive_resource = Resource.objects.create(
            name="Cancha 2",
            resource_type=cls.resource_type,
            is_active=False,
        )

    def _create_reservation(
        self,
        resource=None,
        date_value=None,
        start=None,
        end=None,
        user=None,
        status_value="pending",
    ):
        """Helper to build a Reservation instance and call full_clean()."""
        r = Reservation(
            user=user or self.user,
            resource=resource or self.resource,
            date=date_value or date(2026, 6, 15),
            start_time=start or time(10, 0),
            end_time=end or time(11, 0),
            status=status_value,
        )
        r.full_clean()
        r.save()
        return r

    def test_create_valid_reservation(self):
        reservation = self._create_reservation()
        self.assertEqual(reservation.status, "pending")
        self.assertEqual(reservation.resource, self.resource)

    def test_end_time_before_start_time_raises_error(self):
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start=time(11, 0), end=time(10, 0)
            )

    def test_end_time_equal_to_start_time_raises_error(self):
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start=time(10, 0), end=time(10, 0)
            )

    def test_inactive_resource_raises_error(self):
        with self.assertRaises(ValidationError):
            self._create_reservation(resource=self.inactive_resource)

    def test_exact_overlap_raises_error(self):
        self._create_reservation()
        with self.assertRaises(ValidationError):
            self._create_reservation()

    def test_overlap_start_within_existing_raises_error(self):
        self._create_reservation(start=time(10, 0), end=time(12, 0))
        with self.assertRaises(ValidationError):
            self._create_reservation(start=time(11, 0), end=time(13, 0))

    def test_overlap_end_within_existing_raises_error(self):
        self._create_reservation(start=time(10, 0), end=time(12, 0))
        with self.assertRaises(ValidationError):
            self._create_reservation(start=time(9, 0), end=time(11, 0))

    def test_overlap_encompasses_existing_raises_error(self):
        self._create_reservation(start=time(10, 0), end=time(11, 0))
        with self.assertRaises(ValidationError):
            self._create_reservation(start=time(9, 0), end=time(12, 0))

    def test_different_resource_no_overlap(self):
        other = Resource.objects.create(
            name="Cancha 3",
            resource_type=self.resource_type,
            is_active=True,
        )
        self._create_reservation()
        reservation = self._create_reservation(resource=other)
        self.assertEqual(reservation.resource, other)

    def test_different_date_no_overlap(self):
        self._create_reservation()
        reservation = self._create_reservation(
            date_value=date(2026, 6, 16)
        )
        self.assertEqual(str(reservation.date), "2026-06-16")

    def test_cancelled_reservation_does_not_block_new(self):
        r1 = self._create_reservation()
        r1.status = "cancelled"
        r1.save()
        r2 = self._create_reservation()
        self.assertEqual(r2.status, "pending")

    def test_adjacent_times_no_overlap(self):
        self._create_reservation(start=time(10, 0), end=time(11, 0))
        reservation = self._create_reservation(
            start=time(11, 0), end=time(12, 0)
        )
        self.assertEqual(reservation.start_time, time(11, 0))

    def test_update_to_overlapping_time_raises_error(self):
        self._create_reservation(start=time(10, 0), end=time(11, 0))
        r2 = self._create_reservation(
            start=time(12, 0), end=time(13, 0)
        )
        r2.start_time = time(10, 30)
        r2.end_time = time(11, 30)
        with self.assertRaises(ValidationError):
            r2.full_clean()

    def test_str_representation(self):
        reservation = self._create_reservation()
        expected = "Cancha 1 — 2026-06-15 10:00:00-11:00:00"
        self.assertEqual(str(reservation), expected)


class ReservationAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="apiuser", password="apipass123"
        )
        cls.resource_type = ResourceType.objects.create(name="Salon")
        cls.resource = Resource.objects.create(
            name="Salon A",
            resource_type=cls.resource_type,
            is_active=True,
        )
        cls.list_url = "/api/reservations/"

    def _detail_url(self, pk):
        return f"/api/reservations/{pk}/"

    def _valid_payload(self, **overrides):
        payload = {
            "user": self.user.pk,
            "resource": self.resource.pk,
            "date": "2026-07-01",
            "start_time": "09:00",
            "end_time": "10:00",
        }
        payload.update(overrides)
        return payload

    def test_list_reservations_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_returns_empty_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.data, [])

    def test_create_reservation_returns_201(self):
        response = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["resource_name"], "Salon A")
        self.assertIn("id", response.data)

    def test_create_with_overlap_returns_400(self):
        self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        response = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_end_time_before_start_returns_400(self):
        response = self.client.post(
            self.list_url,
            self._valid_payload(start_time="11:00", end_time="10:00"),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_inactive_resource_returns_400(self):
        inactive = Resource.objects.create(
            name="Salon B",
            resource_type=self.resource_type,
            is_active=False,
        )
        response = self.client.post(
            self.list_url,
            self._valid_payload(resource=inactive.pk),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_missing_fields_returns_400(self):
        response = self.client.post(
            self.list_url, {"user": self.user.pk}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_detail_returns_200(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.get(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["resource_name"], "Salon A")

    def test_get_detail_not_found_returns_404(self):
        response = self.client.get(self._detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_status_returns_200(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.patch(
            self._detail_url(pk),
            {"status": "confirmed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "confirmed")

    def test_patch_to_overlap_returns_400(self):
        r1 = self.client.post(
            self.list_url,
            self._valid_payload(
                start_time="09:00", end_time="10:00"
            ),
            format="json",
        )
        r2 = self.client.post(
            self.list_url,
            self._valid_payload(
                start_time="11:00", end_time="12:00"
            ),
            format="json",
        )
        response = self.client.patch(
            self._detail_url(r2.data["id"]),
            {"start_time": "09:30", "end_time": "10:30"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_returns_created_reservations(self):
        self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        self.client.post(
            self.list_url,
            self._valid_payload(
                start_time="11:00", end_time="12:00"
            ),
            format="json",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 2)

    def test_delete_reservation_returns_204(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.delete(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_reservation_removes_it(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        self.client.delete(self._detail_url(pk))
        get_resp = self.client.get(self._detail_url(pk))
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_returns_404(self):
        response = self.client.delete(self._detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_method_not_allowed_on_list(self):
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
