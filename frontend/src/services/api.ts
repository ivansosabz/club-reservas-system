const API_BASE_URL = "http://localhost:8000/api";

function extractErrorMessages(errorData: unknown): string {
  if (typeof errorData !== "object" || errorData === null) {
    return String(errorData);
  }

  const obj = errorData as Record<string, unknown>;

  if (typeof obj.detail === "string") {
    return obj.detail;
  }

  if (Array.isArray(obj.non_field_errors)) {
    return obj.non_field_errors.join(" ");
  }

  const messages: string[] = [];

  for (const [field, value] of Object.entries(obj)) {
    if (field === "non_field_errors") continue;

    if (Array.isArray(value)) {
      messages.push(value.join(" "));
    } else if (typeof value === "string") {
      messages.push(`${field}: ${value}`);
    }
  }

  return messages.length > 0 ? messages.join(" ") : JSON.stringify(errorData);
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("token");

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      throw new Error("Sesión expirada. Inicia sesión nuevamente.");
    }

    let errorMessage = "Ocurrió un error en la petición";

    try {
      const errorData = await response.json();
      errorMessage = extractErrorMessages(errorData);
    } catch {
      errorMessage = response.statusText || errorMessage;
    }

    throw new Error(errorMessage);
  }

  if (response.status === 204) {
    return null as T;
  }

  return response.json();
}

export function buildQueryString(
  params: Record<string, string | number | undefined>
): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") {
      search.set(key, String(value));
    }
  }
  const str = search.toString();
  return str ? `?${str}` : "";
}

export { API_BASE_URL };