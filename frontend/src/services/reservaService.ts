import { apiFetch } from "./api";
import type { Reserva, CrearReservaPayload } from "../types/reserva";

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
