/* eslint-disable react-refresh/only-export-components */

import { createContext, useCallback, useContext, useState } from "react";
import type { ReactNode } from "react";
import * as authService from "../services/authService";

interface User {
  id: number;
  username: string;
  email?: string;
  is_staff?: boolean;
}

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function decodeToken(token: string): User | null {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return {
      id: payload.user_id,
      username: payload.username,
      is_staff: payload.is_staff ?? false,
    };
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const token = authService.getToken();
    return token ? decodeToken(token) : null;
  });

  const login = useCallback(async (username: string, password: string) => {
    const response = await authService.login({ username, password });

    if (!response.access) {
      throw new Error("No se recibio el token de acceso.");
    }

    authService.saveToken(response.access);
    const decoded = decodeToken(response.access);
    setUser(decoded);
  }, []);

  const register = useCallback(
    async (username: string, email: string, password: string) => {
      const response = await authService.register({
        username,
        email,
        password,
      });

      if (!response.access) {
        throw new Error("No se recibio el token de acceso.");
      }

      authService.saveToken(response.access);
      const decoded = decodeToken(response.access);
      setUser(decoded);
    },
    []
  );

  const logout = useCallback(() => {
    authService.removeToken();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: user !== null,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth debe usarse dentro de un AuthProvider");
  }

  return context;
}
