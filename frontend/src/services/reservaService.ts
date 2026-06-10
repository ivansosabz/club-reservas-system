import { apiFetch } from "./api";
import type {
  ActualizarReservaPayload,
  CrearReservaPayload,
  Reserva,
} from "../types/reserva";

export async function getReservas(): Promise<Reserva[]> {
  return apiFetch<Reserva[]>("/reservations/");
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
