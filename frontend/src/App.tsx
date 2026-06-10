import { useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AboutPage from "./pages/AboutPage";
import ProfileModal from "./components/ProfileModal";
import AdminResourcesPage from "./pages/AdminResourcesPage";
import AdminResourceTypesPage from "./pages/AdminResourceTypesPage";
import LoginPage from "./pages/LoginPage";
import NewReservationPage from "./pages/NewReservationPage";
import RegisterPage from "./pages/RegisterPage";
import ReservationsPage from "./pages/ReservationsPage";
import "./App.css";

function NavBar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [profileOpen, setProfileOpen] = useState(false);

  return (
    <nav className="main-nav">
      <div className="brand-mark">Club Reservas</div>

      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <NavLink className="nav-link" to="/">
              Reservas
            </NavLink>
            <NavLink className="nav-link" to="/new">
              Nueva reserva
            </NavLink>
            <NavLink className="nav-link" to="/recursos">
              Recursos
            </NavLink>
            {user?.is_staff ? (
              <NavLink className="nav-link" to="/tipos-de-recurso">
                Tipos de recurso
              </NavLink>
            ) : null}
            <NavLink className="nav-link" to="/about">
              Acerca de
            </NavLink>
            <span
              className="nav-link nav-dropdown-trigger"
              onClick={() => setProfileOpen(true)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === "Enter" && setProfileOpen(true)}
            >
              {user?.username}
            </span>
            <button className="nav-link" onClick={logout} style={{ cursor: "pointer", border: "none", background: "none" }}>
              Salir
            </button>
          </>
        ) : (
          <>
            <NavLink className="nav-link" to="/login">
              Ingresar
            </NavLink>
            <NavLink className="nav-link" to="/register">
              Registrarse
            </NavLink>
            <NavLink className="nav-link" to="/about">
              Acerca de
            </NavLink>
          </>
        )}
      </div>

      <ProfileModal open={profileOpen} onClose={() => setProfileOpen(false)} />
    </nav>
  );
}

function AppContent() {
  return (
    <div className="app-shell">
      <div className="app-layout">
        <NavBar />

        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <ReservationsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/new"
            element={
              <ProtectedRoute>
                <NewReservationPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recursos"
            element={
              <ProtectedRoute>
                <AdminResourcesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/tipos-de-recurso"
            element={
              <ProtectedRoute>
                <AdminResourceTypesPage />
              </ProtectedRoute>
            }
          />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
