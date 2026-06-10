export interface Reserva {
  id: number;
  user: number;
  user_username?: string;
  resource: number;
  resource_name?: string;
  date: string;
  start_time: string;
  end_time: string;
  status?: string;
  notes?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface CrearReservaPayload {
  user: number;
  resource: number;
  date: string;
  start_time: string;
  end_time: string;
  notes?: string;
}

export interface ActualizarReservaPayload {
  resource?: number;
  date?: string;
  start_time?: string;
  end_time?: string;
  status?: string;
  notes?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ReservaFilters {
  page?: number;
  page_size?: number;
  date_from?: string;
  date_to?: string;
  status?: string;
  resource?: number;
  search?: string;
  ordering?: string;
}
