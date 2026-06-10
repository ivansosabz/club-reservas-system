import { apiFetch, buildQueryString } from "./api";
import type {
  ActualizarReservaPayload,
  CrearReservaPayload,
  PaginatedResponse,
  Reserva,
  ReservaFilters,
} from "../types/reserva";

export async function getReservas(
  filters?: ReservaFilters
): Promise<PaginatedResponse<Reserva>> {
  const query = filters ? buildQueryString(filters as Record<string, string | number | undefined>) : "";
  return apiFetch<PaginatedResponse<Reserva>>(`/reservations/${query}`);
}

export async function crearReserva(
  payload: CrearReservaPayload
): Promise<Reserva> {
  return apiFetch<Reserva>("/reservations/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function actualizarReserva(
  id: number,
  payload: ActualizarReservaPayload
): Promise<Reserva> {
  return apiFetch<Reserva>(`/reservations/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function eliminarReserva(id: number): Promise<void> {
  await apiFetch<void>(`/reservations/${id}/`, {
    method: "DELETE",
  });
}
