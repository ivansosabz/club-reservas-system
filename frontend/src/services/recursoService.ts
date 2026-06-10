import { apiFetch } from "./api";
import type {
  CrearRecursoPayload,
  CrearTipoRecursoPayload,
  Recurso,
  TipoRecurso,
} from "../types/recurso";

export async function getRecursos(todas?: boolean): Promise<Recurso[]> {
  const query = todas ? "?todas=true" : "";
  return apiFetch<Recurso[]>(`/resources/${query}`);
}

export async function obtenerRecurso(id: number): Promise<Recurso> {
  return apiFetch<Recurso>(`/resources/${id}/`);
}

export async function crearRecurso(
  data: CrearRecursoPayload
): Promise<Recurso> {
  return apiFetch<Recurso>("/resources/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function actualizarRecurso(
  id: number,
  data: Partial<CrearRecursoPayload>
): Promise<Recurso> {
  return apiFetch<Recurso>(`/resources/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function eliminarRecurso(id: number): Promise<void> {
  await apiFetch<void>(`/resources/${id}/`, { method: "DELETE" });
}

export async function getTiposRecurso(): Promise<TipoRecurso[]> {
  return apiFetch<TipoRecurso[]>("/resource-types/");
}

export async function obtenerTipoRecurso(id: number): Promise<TipoRecurso> {
  return apiFetch<TipoRecurso>(`/resource-types/${id}/`);
}

export async function crearTipoRecurso(
  data: CrearTipoRecursoPayload
): Promise<TipoRecurso> {
  return apiFetch<TipoRecurso>("/resource-types/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function actualizarTipoRecurso(
  id: number,
  data: Partial<CrearTipoRecursoPayload>
): Promise<TipoRecurso> {
  return apiFetch<TipoRecurso>(`/resource-types/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function eliminarTipoRecurso(id: number): Promise<void> {
  await apiFetch<void>(`/resource-types/${id}/`, { method: "DELETE" });
}
