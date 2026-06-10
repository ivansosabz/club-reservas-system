export interface Recurso {
  id: number;
  name: string;
  resource_type: number;
  resource_type_name?: string;
  description?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface TipoRecurso {
  id: number;
  name: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CrearRecursoPayload {
  name: string;
  resource_type: number;
  description?: string;
  is_active?: boolean;
}

export interface CrearTipoRecursoPayload {
  name: string;
  description?: string;
}
