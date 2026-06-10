import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

function LoginPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");

    if (!username || !password) {
      setError("Completa todos los campos.");
      return;
    }

    setLoading(true);

    try {
      await login(username, password);
      navigate("/");
    } catch (loginError) {
      setError(
        loginError instanceof Error
          ? loginError.message
          : "Error al iniciar sesion."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page">
      <header className="page-header">
        <p className="page-kicker">Acceso</p>
        <h1 className="page-title">Iniciar sesion</h1>
        <p className="page-description">
          Ingresa con tu usuario y contrasena para gestionar las reservas.
        </p>
      </header>

      {error ? (
        <p className="status-text status-text--error">{error}</p>
      ) : null}

      <form
        onSubmit={handleSubmit}
        className="panel-card new-reservation-form"
      >
        <div className="form-group">
          <label>Usuario</label>
          <input
            className="form-input"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            autoFocus
          />
        </div>

        <div className="form-group">
          <label>Contrasena</label>
          <input
            className="form-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
        </div>

        <button
          type="submit"
          className="primary-button"
          disabled={loading}
        >
          {loading ? "Ingresando..." : "Ingresar"}
        </button>

        <p style={{ textAlign: "center", color: "var(--app-muted)", fontSize: "14px" }}>
          No tenes cuenta?{" "}
          <Link to="/register" style={{ color: "var(--app-accent)" }}>
            Registrate
          </Link>
        </p>
      </form>
    </section>
  );
}

export default LoginPage;
