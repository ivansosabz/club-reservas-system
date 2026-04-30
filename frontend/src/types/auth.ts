export interface LoginPayload {
  username: string;
  password: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access?: string;
  refresh?: string;
  token?: string;
  message?: string;
}