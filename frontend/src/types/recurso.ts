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
