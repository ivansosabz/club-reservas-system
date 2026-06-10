import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

function RegisterPage() {
  const navigate = useNavigate();
  const { register, isAuthenticated } = useAuth();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError("");

    if (!username || !email || !password || !password2) {
      setError("Completa todos los campos.");
      return;
    }

    if (password !== password2) {
      setError("Las contrasenas no coinciden.");
      return;
    }

    setLoading(true);

    try {
      await register(username, email, password);
      navigate("/");
    } catch (registerError) {
      setError(
        registerError instanceof Error
          ? registerError.message
          : "Error al registrarse."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page">
      <header className="page-header">
        <p className="page-kicker">Nuevo acceso</p>
        <h1 className="page-title">Registrarse</h1>
        <p className="page-description">
          Crea una cuenta para empezar a reservar espacios del club.
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
          <label>Email</label>
          <input
            className="form-input"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
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

        <div className="form-group">
          <label>Confirmar contrasena</label>
          <input
            className="form-input"
            type="password"
            value={password2}
            onChange={(event) => setPassword2(event.target.value)}
          />
        </div>

        <button
          type="submit"
          className="primary-button"
          disabled={loading}
        >
          {loading ? "Registrando..." : "Crear cuenta"}
        </button>

        <p style={{ textAlign: "center", color: "var(--app-muted)", fontSize: "14px" }}>
          Ya tenes cuenta?{" "}
          <Link to="/login" style={{ color: "var(--app-accent)" }}>
            Inicia sesion
          </Link>
        </p>
      </form>
    </section>
  );
}

export default RegisterPage;
