from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer, ReservationUpdateSerializer


class ReservationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET", "POST"])
def reservation_list_create(request):
    if request.method == "GET":
        queryset = Reservation.objects.select_related("resource", "user")

        date_from = request.query_params.get("date_from")
        if date_from:
            queryset = queryset.filter(start_datetime__gte=date_from)

        date_to = request.query_params.get("date_to")
        if date_to:
            queryset = queryset.filter(start_datetime__lte=date_to)

        status_param = request.query_params.get("status")
        if status_param:
            statuses = status_param.split(",")
            queryset = queryset.filter(status__in=statuses)

        end_from = request.query_params.get("end_from")
        if end_from:
            queryset = queryset.filter(end_datetime__gte=end_from)

        end_to = request.query_params.get("end_to")
        if end_to:
            queryset = queryset.filter(end_datetime__lte=end_to)

        resource = request.query_params.get("resource")
        if resource:
            queryset = queryset.filter(resource_id=resource)

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(resource__name__icontains=search)
                | Q(user__username__icontains=search)
            )

        ordering = request.query_params.get("ordering", "start_datetime")
        queryset = queryset.order_by(ordering)

        paginator = ReservationPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ReservationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = ReservationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def reservation_detail_update(request, pk):
    reservation = get_object_or_404(
        Reservation.objects.select_related("resource", "user"),
        pk=pk,
    )

    if request.method == "GET":
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    if request.method == "DELETE":
        if not request.user.is_staff:
            return Response(
                {"detail": "Solo el administrador puede eliminar reservas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if not request.user.is_staff:
        if reservation.user != request.user:
            return Response(
                {"detail": "Solo puedes editar tus propias reservas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if reservation.status != "pending":
            return Response(
                {"detail": "Solo puedes editar reservas pendientes."},
                status=status.HTTP_403_FORBIDDEN,
            )

    serializer = ReservationUpdateSerializer(
        reservation,
        data=request.data,
        partial=True,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
