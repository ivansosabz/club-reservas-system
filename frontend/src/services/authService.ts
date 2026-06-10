import { apiFetch } from "./api";
import type { AuthResponse, LoginPayload, RegisterPayload } from "../types/auth";

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  return apiFetch<AuthResponse>("/auth/login/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function register(payload: RegisterPayload): Promise<AuthResponse> {
  return apiFetch<AuthResponse>("/auth/register/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export interface ProfileData {
  id: number;
  username: string;
  email: string;
  phone: string | null;
}

export async function getProfile(): Promise<ProfileData> {
  return apiFetch<ProfileData>("/auth/profile/", {
    method: "GET",
  });
}

export async function updateProfile(data: Partial<Pick<ProfileData, "email" | "phone">>): Promise<ProfileData> {
  return apiFetch<ProfileData>("/auth/profile/", {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function saveToken(token: string) {
  localStorage.setItem("token", token);
}

export function removeToken() {
  localStorage.removeItem("token");
}

export function getToken() {
  return localStorage.getItem("token");
}

export function isAuthenticated() {
  return !!getToken();
}