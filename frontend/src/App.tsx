import { NavLink, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AboutPage from "./pages/AboutPage";
import AdminResourcesPage from "./pages/AdminResourcesPage";
import AdminResourceTypesPage from "./pages/AdminResourceTypesPage";
import LoginPage from "./pages/LoginPage";
import NewReservationPage from "./pages/NewReservationPage";
import RegisterPage from "./pages/RegisterPage";
import ReservationsPage from "./pages/ReservationsPage";
import "./App.css";

function NavBar() {
  const { user, isAuthenticated, logout } = useAuth();

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
            <div className="nav-dropdown">
              <span className="nav-link nav-dropdown-trigger">
                Recursos
              </span>
              <div className="nav-dropdown-menu">
                <NavLink className="nav-dropdown-item" to="/recursos">
                  Gestionar recursos
                </NavLink>
                <NavLink className="nav-dropdown-item" to="/tipos-de-recurso">
                  Tipos de recurso
                </NavLink>
              </div>
            </div>
            <NavLink className="nav-link" to="/about">
              Acerca de
            </NavLink>
            <span className="nav-link" style={{ opacity: 0.6 }}>
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
