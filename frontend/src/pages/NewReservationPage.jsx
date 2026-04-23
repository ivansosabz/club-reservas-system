import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  createReservation,
  getResources,
} from "../services/reservationsService";
import "./NewReservationPage.css";

// Placeholder hasta que haya autenticación (Etapa 5).
// Mientras tanto el backend requiere un user id — usamos el admin (id=1)
// o el que tengas creado. Cambialo si hace falta.
const PLACEHOLDER_USER_ID = 1;

function NewReservationPage({ reservations, setReservations }) {
  const navigate = useNavigate();

  // Lista de recursos para el select.
  const [resources, setResources] = useState([]);

  // Estado del formulario. Nombres alineados con el backend.
  const [resource, setResource] = useState("");
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getResources()
      .then(setResources)
      .catch((err) => setError(err.message));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    if (!resource || !date || !startTime || !endTime) {
      setError("Completá todos los campos");
      return;
    }

    if (startTime >= endTime) {
      setError("La hora de inicio debe ser menor a la de fin");
      return;
    }

    const payload = {
      user: PLACEHOLDER_USER_ID,
      resource: Number(resource),
      date,
      start_time: startTime,
      end_time: endTime,
    };

    try {
      setSubmitting(true);
      const nueva = await createReservation(payload);
      setReservations([...reservations, nueva]);
      navigate("/");
    } catch (err) {
      // El back devuelve errores en `err.data` (ej: solape, recurso inactivo).
      const backendMsg = err.data
        ? JSON.stringify(err.data)
        : err.message;
      setError(backendMsg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="new-reservation-page">
      <header className="page-header">
        <p className="page-kicker">Nuevo turno</p>
        <h1 className="page-title">Nueva reserva</h1>
        <p className="page-description">
          Completa los datos del recurso y define el horario de uso.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="panel-card new-reservation-form">
        <div className="form-group">
          <label>Recurso</label>
          <select
            className="form-input"
            value={resource}
            onChange={(e) => setResource(e.target.value)}
          >
            <option value="">Seleccioná un recurso</option>
            {resources.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.resource_type_name})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Fecha</label>
          <input
            className="form-input"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="time-grid">
          <div className="form-group">
            <label>Hora de inicio</label>
            <input
              className="form-input"
              type="time"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Hora de fin</label>
            <input
              className="form-input"
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            />
          </div>
        </div>

        {error && <p className="status-text">Error: {error}</p>}

        <button
          type="submit"
          className="primary-button"
          disabled={submitting}
        >
          {submitting ? "Guardando..." : "Guardar reserva"}
        </button>
      </form>
    </section>
  );
}

export default NewReservationPage;
