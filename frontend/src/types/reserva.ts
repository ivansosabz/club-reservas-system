export interface Reserva {
  id: number;
  user: number;
  user_username?: string;
  user_email?: string | null;
  user_phone?: string | null;
  resource: number;
  resource_name?: string;
  start_datetime: string;
  end_datetime: string;
  status?: string;
  notes?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface CrearReservaPayload {
  user: number;
  resource: number;
  start_datetime: string;
  end_datetime: string;
  notes?: string;
}

export interface ActualizarReservaPayload {
  resource?: number;
  start_datetime?: string;
  end_datetime?: string;
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
  end_from?: string;
  end_to?: string;
  status?: string;
  resource?: number;
  search?: string;
  ordering?: string;
}
