export interface Reserva {
  id: number;
  recurso: number;
  usuario?: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  estado?: string;
}

export interface CrearReservaPayload {
  recurso: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
}