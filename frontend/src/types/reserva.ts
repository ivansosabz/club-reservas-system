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
