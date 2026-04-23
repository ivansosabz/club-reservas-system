import { apiFetch } from "./api";
import type { Recurso } from "../types/recurso";

export async function getRecursos(): Promise<Recurso[]> {
  return apiFetch<Recurso[]>("/resources/");
}
