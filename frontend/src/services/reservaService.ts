import { apiFetch } from "./api";
import type { Reserva, CrearReservaPayload } from "../types/reserva";

export async function getReservas(): Promise<Reserva[]> {
  return apiFetch<Reserva[]>("/reservas/");
}

export async function getReservaById(id: number): Promise<Reserva> {
  return apiFetch<Reserva>(`/reservas/${id}/`);
}

export async function crearReserva(
  payload: CrearReservaPayload
): Promise<Reserva> {
  return apiFetch<Reserva>("/reservas/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function eliminarReserva(id: number): Promise<void> {
  return apiFetch<void>(`/reservas/${id}/`, {
    method: "DELETE",
  });
}
