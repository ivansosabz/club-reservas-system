from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from resources.models import Resource, ResourceType
from .models import Reservation


def _dt(*args):
    return timezone.make_aware(datetime(*args))


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
        start_dt=None,
        end_dt=None,
        user=None,
        status_value="pending",
    ):
        r = Reservation(
            user=user or self.user,
            resource=resource or self.resource,
            start_datetime=start_dt or _dt(2026, 6, 15, 10, 0),
            end_datetime=end_dt or _dt(2026, 6, 15, 11, 0),
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
                start_dt=_dt(2026, 6, 15, 11, 0),
                end_dt=_dt(2026, 6, 15, 10, 0),
            )

    def test_end_time_equal_to_start_time_raises_error(self):
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start_dt=_dt(2026, 6, 15, 10, 0),
                end_dt=_dt(2026, 6, 15, 10, 0),
            )

    def test_inactive_resource_raises_error(self):
        with self.assertRaises(ValidationError):
            self._create_reservation(resource=self.inactive_resource)

    def test_exact_overlap_raises_error(self):
        self._create_reservation()
        with self.assertRaises(ValidationError):
            self._create_reservation()

    def test_overlap_start_within_existing_raises_error(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 15, 10, 0),
            end_dt=_dt(2026, 6, 15, 12, 0),
        )
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start_dt=_dt(2026, 6, 15, 11, 0),
                end_dt=_dt(2026, 6, 15, 13, 0),
            )

    def test_overlap_end_within_existing_raises_error(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 15, 10, 0),
            end_dt=_dt(2026, 6, 15, 12, 0),
        )
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start_dt=_dt(2026, 6, 15, 9, 0),
                end_dt=_dt(2026, 6, 15, 11, 0),
            )

    def test_overlap_encompasses_existing_raises_error(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 15, 10, 0),
            end_dt=_dt(2026, 6, 15, 11, 0),
        )
        with self.assertRaises(ValidationError):
            self._create_reservation(
                start_dt=_dt(2026, 6, 15, 9, 0),
                end_dt=_dt(2026, 6, 15, 12, 0),
            )

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
            start_dt=_dt(2026, 6, 16, 10, 0),
            end_dt=_dt(2026, 6, 16, 11, 0),
        )
        self.assertEqual(reservation.start_datetime.date().isoformat(), "2026-06-16")

    def test_cancelled_reservation_does_not_block_new(self):
        r1 = self._create_reservation()
        r1.status = "cancelled"
        r1.save()
        r2 = self._create_reservation()
        self.assertEqual(r2.status, "pending")

    def test_adjacent_times_no_overlap(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 15, 10, 0),
            end_dt=_dt(2026, 6, 15, 11, 0),
        )
        reservation = self._create_reservation(
            start_dt=_dt(2026, 6, 15, 11, 0),
            end_dt=_dt(2026, 6, 15, 12, 0),
        )
        self.assertEqual(reservation.start_datetime, _dt(2026, 6, 15, 11, 0))

    def test_update_to_overlapping_time_raises_error(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 15, 10, 0),
            end_dt=_dt(2026, 6, 15, 11, 0),
        )
        r2 = self._create_reservation(
            start_dt=_dt(2026, 6, 15, 12, 0),
            end_dt=_dt(2026, 6, 15, 13, 0),
        )
        r2.start_datetime = _dt(2026, 6, 15, 10, 30)
        r2.end_datetime = _dt(2026, 6, 15, 11, 30)
        with self.assertRaises(ValidationError):
            r2.full_clean()

    def test_create_multi_day_reservation(self):
        r = Reservation(
            user=self.user,
            resource=self.resource,
            start_datetime=_dt(2026, 6, 10, 10, 0),
            end_datetime=_dt(2026, 6, 12, 18, 0),
        )
        r.full_clean()
        r.save()
        self.assertEqual(r.end_datetime, _dt(2026, 6, 12, 18, 0))

    def test_end_date_before_start_date_raises_error(self):
        with self.assertRaises(ValidationError):
            r = Reservation(
                user=self.user,
                resource=self.resource,
                start_datetime=_dt(2026, 6, 15, 10, 0),
                end_datetime=_dt(2026, 6, 14, 11, 0),
            )
            r.full_clean()

    def test_multi_day_overlap_with_single_day(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 10, 10, 0),
            end_dt=_dt(2026, 6, 10, 12, 0),
        )
        with self.assertRaises(ValidationError):
            r = Reservation(
                user=self.user,
                resource=self.resource,
                start_datetime=_dt(2026, 6, 9, 8, 0),
                end_datetime=_dt(2026, 6, 11, 18, 0),
            )
            r.full_clean()

    def test_multi_day_no_overlap_when_ends_before(self):
        self._create_reservation(
            start_dt=_dt(2026, 6, 12, 10, 0),
            end_dt=_dt(2026, 6, 12, 12, 0),
        )
        r = Reservation(
            user=self.user,
            resource=self.resource,
            start_datetime=_dt(2026, 6, 9, 8, 0),
            end_datetime=_dt(2026, 6, 11, 20, 0),
        )
        r.full_clean()
        r.save()
        self.assertEqual(r.end_datetime, _dt(2026, 6, 11, 20, 0))

    def test_str_representation(self):
        reservation = self._create_reservation()
        expected = "Cancha 1 — 15/06 10:00-15/06 11:00"
        self.assertEqual(str(reservation), expected)


class ReservationAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="apiuser", password="apipass123"
        )
        cls.other_user = User.objects.create_user(
            username="mateo", password="pass123"
        )
        cls.staff_user = User.objects.create_user(
            username="staff", password="staffpass123", is_staff=True
        )
        cls.resource_type = ResourceType.objects.create(name="Salon")
        cls.resource = Resource.objects.create(
            name="Salon A",
            resource_type=cls.resource_type,
            is_active=True,
        )
        cls.other_resource = Resource.objects.create(
            name="Salon B",
            resource_type=cls.resource_type,
            is_active=True,
        )
        cls.list_url = "/api/reservations/"

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def _detail_url(self, pk):
        return f"/api/reservations/{pk}/"

    def _valid_payload(self, **overrides):
        payload = {
            "user": self.user.pk,
            "resource": self.resource.pk,
            "start_datetime": "2026-07-01T09:00:00",
            "end_datetime": "2026-07-01T10:00:00",
        }
        payload.update(overrides)
        return payload

    def test_list_reservations_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_returns_paginated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.data["count"], 0)

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
            self._valid_payload(
                start_datetime="2026-07-01T11:00:00",
                end_datetime="2026-07-01T10:00:00",
            ),
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

    def test_create_multi_day_returns_201(self):
        response = self.client.post(
            self.list_url,
            self._valid_payload(
                start_datetime="2026-07-01T09:00:00",
                end_datetime="2026-07-03T18:00:00",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["end_datetime"][:10], "2026-07-03")

    def test_create_multi_day_invalid_date_order_returns_400(self):
        response = self.client.post(
            self.list_url,
            self._valid_payload(
                start_datetime="2026-07-05T09:00:00",
                end_datetime="2026-07-03T10:00:00",
            ),
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
        self.client.force_authenticate(user=self.staff_user)
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
                start_datetime="2026-07-01T09:00:00",
                end_datetime="2026-07-01T10:00:00",
            ),
            format="json",
        )
        r2 = self.client.post(
            self.list_url,
            self._valid_payload(
                start_datetime="2026-07-01T11:00:00",
                end_datetime="2026-07-01T12:00:00",
            ),
            format="json",
        )
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.patch(
            self._detail_url(r2.data["id"]),
            {"start_datetime": "2026-07-01T09:30:00", "end_datetime": "2026-07-01T10:30:00"},
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
                start_datetime="2026-07-01T11:00:00",
                end_datetime="2026-07-01T12:00:00",
            ),
            format="json",
        )
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["count"], 2)

    def test_delete_reservation_returns_204(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_reservation_removes_it(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        self.client.force_authenticate(user=self.staff_user)
        self.client.delete(self._detail_url(pk))
        self.client.force_authenticate(user=self.user)
        get_resp = self.client.get(self._detail_url(pk))
        self.assertEqual(get_resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_returns_404(self):
        response = self.client.delete(self._detail_url(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_method_not_allowed_on_list(self):
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_owner_can_patch_when_pending(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.patch(
            self._detail_url(pk),
            {"notes": "Actualizado por el dueno"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notes"], "Actualizado por el dueno")

    def test_owner_cannot_patch_when_confirmed(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        Reservation.objects.filter(pk=pk).update(status="confirmed")
        response = self.client.patch(
            self._detail_url(pk),
            {"notes": "Intento"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_cannot_patch_others_reservation(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        self.client.force_authenticate(user=self.other_user)
        response = self.client.patch(
            self._detail_url(pk),
            {"notes": "Intento ajeno"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_patch(self):
        self.client.force_authenticate(user=self.staff_user)
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

    def test_staff_can_change_resource(self):
        self.client.force_authenticate(user=self.staff_user)
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.patch(
            self._detail_url(pk),
            {"resource": self.other_resource.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["resource"], self.other_resource.pk)

    def test_non_staff_get_returns_200(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.get(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_date_from(self):
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-01T09:00:00", end_datetime="2026-07-01T10:00:00"), format="json"
        )
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-05T09:00:00", end_datetime="2026-07-05T10:00:00"), format="json"
        )
        response = self.client.get(
            self.list_url, {"date_from": "2026-07-03"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_date_range(self):
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-01T09:00:00", end_datetime="2026-07-01T10:00:00"), format="json"
        )
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-10T09:00:00", end_datetime="2026-07-10T10:00:00"), format="json"
        )
        response = self.client.get(
            self.list_url, {"date_from": "2026-07-01", "date_to": "2026-07-05"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_status(self):
        self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        self.client.post(
            self.list_url,
            self._valid_payload(start_datetime="2026-07-01T11:00:00", end_datetime="2026-07-01T12:00:00"),
            format="json",
        )
        r1 = Reservation.objects.first()
        r1.status = "confirmed"
        r1.save()
        response = self.client.get(
            self.list_url, {"status": "confirmed"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_resource(self):
        self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        self.client.post(
            self.list_url,
            self._valid_payload(resource=self.other_resource.pk),
            format="json",
        )
        response = self.client.get(
            self.list_url, {"resource": self.other_resource.pk}
        )
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_search(self):
        self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        response = self.client.get(
            self.list_url, {"search": "Salon A"}
        )
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(
            self.list_url, {"search": "apiuser"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_pagination_default_page_size(self):
        for i in range(25):
            h = 9 + i // 60
            m = i % 60
            self.client.post(
                self.list_url,
                self._valid_payload(
                    start_datetime=f"2026-07-01T{h:02d}:{m:02d}:00",
                    end_datetime=f"2026-07-01T{h:02d}:{m + 1:02d}:00",
                ),
                format="json",
            )
        response = self.client.get(self.list_url)
        self.assertEqual(response.data["count"], 25)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

    def test_pagination_custom_page_size(self):
        for i in range(10):
            h = 9 + i // 60
            m = i % 60
            self.client.post(
                self.list_url,
                self._valid_payload(
                    start_datetime=f"2026-07-01T{h:02d}:{m:02d}:00",
                    end_datetime=f"2026-07-01T{h:02d}:{m + 1:02d}:00",
                ),
                format="json",
            )
        response = self.client.get(
            self.list_url, {"page_size": "5"}
        )
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["count"], 10)
        self.assertIsNotNone(response.data["next"])

    def test_pagination_second_page(self):
        for i in range(25):
            h = 9 + i // 60
            m = i % 60
            self.client.post(
                self.list_url,
                self._valid_payload(
                    start_datetime=f"2026-07-01T{h:02d}:{m:02d}:00",
                    end_datetime=f"2026-07-01T{h:02d}:{m + 1:02d}:00",
                ),
                format="json",
            )
        response = self.client.get(
            self.list_url, {"page": "2", "page_size": "10"}
        )
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["previous"])

    def test_ordering_desc(self):
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-01T09:00:00", end_datetime="2026-07-01T10:00:00"), format="json"
        )
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-10T09:00:00", end_datetime="2026-07-10T10:00:00"), format="json"
        )
        response = self.client.get(
            self.list_url, {"ordering": "-start_datetime"}
        )
        results = response.data["results"]
        self.assertEqual(results[0]["start_datetime"][:10], "2026-07-10")
        self.assertEqual(results[1]["start_datetime"][:10], "2026-07-01")

    def test_filter_by_end_from(self):
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-01T09:00:00", end_datetime="2026-07-01T10:00:00"), format="json"
        )
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-05T09:00:00", end_datetime="2026-07-05T10:00:00"), format="json"
        )
        response = self.client.get(
            self.list_url, {"end_from": "2026-07-03T00:00:00"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_end_to(self):
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-01T09:00:00", end_datetime="2026-07-01T10:00:00"), format="json"
        )
        self.client.post(
            self.list_url, self._valid_payload(start_datetime="2026-07-05T09:00:00", end_datetime="2026-07-05T10:00:00"), format="json"
        )
        response = self.client.get(
            self.list_url, {"end_to": "2026-07-03T00:00:00"}
        )
        self.assertEqual(response.data["count"], 1)

    def test_non_staff_delete_returns_403(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        response = self.client.delete(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_delete(self):
        create_resp = self.client.post(
            self.list_url, self._valid_payload(), format="json"
        )
        pk = create_resp.data["id"]
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self._detail_url(pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
