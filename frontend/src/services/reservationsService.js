// Servicios para hablar con la API del backend (Django + DRF).
//
// Las URLs son absolutas contra el back local (Django suele correr en 8000).
// Más adelante conviene centralizarlas en una variable de entorno de Vite
// (import.meta.env.VITE_API_URL), pero por ahora lo dejamos explícito.

const API_BASE = "http://localhost:8000/api";

// ------------------------------
// Reservas
// ------------------------------

export async function getReservations() {
  const res = await fetch(`${API_BASE}/reservations/`);
  if (!res.ok) throw new Error("No se pudo traer la lista de reservas");
  return res.json();
}

export async function createReservation(payload) {
  // `payload` debe tener la forma esperada por el backend:
  // { user, resource, date, start_time, end_time, notes? }
  const res = await fetch(`${API_BASE}/reservations/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    // El back devuelve errores de validación como JSON — los pasamos tal cual
    // para que la UI pueda mostrarlos (ej: "ya existe una reserva...").
    const errorData = await res.json().catch(() => ({}));
    const err = new Error("No se pudo crear la reserva");
    err.data = errorData;
    throw err;
  }

  return res.json();
}

// ------------------------------
// Recursos (para el select del formulario)
// ------------------------------

export async function getResources() {
  const res = await fetch(`${API_BASE}/resources/`);
  if (!res.ok) throw new Error("No se pudo traer la lista de recursos");
  return res.json();
}
