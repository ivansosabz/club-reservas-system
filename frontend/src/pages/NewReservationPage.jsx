import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRecursos } from "../services/recursoService";
import { crearReserva } from "../services/reservaService";
import "./NewReservationPage.css";

const DEFAULT_USER_ID = 1;

function NewReservationPage() {
  const navigate = useNavigate();
  const [resource, setResource] = useState("");
  const [resources, setResources] = useState([]);
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [loadingResources, setLoadingResources] = useState(true);
  const [resourceError, setResourceError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isActive = true;

    async function loadResources() {
      try {
        const data = await getRecursos();

        if (!isActive) {
          return;
        }

        setResources(data);
        setResourceError("");
      } catch (loadError) {
        if (!isActive) {
          return;
        }

        setResourceError(
          loadError instanceof Error
            ? loadError.message
            : "No se pudieron cargar los recursos."
        );
      } finally {
        if (isActive) {
          setLoadingResources(false);
        }
      }
    }

    void loadResources();

    return () => {
      isActive = false;
    };
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitError("");

    if (!resource || !date || !startTime || !endTime) {
      setSubmitError("Completa todos los campos.");
      return;
    }

    if (startTime >= endTime) {
      setSubmitError("La hora de inicio debe ser menor a la de fin.");
      return;
    }

    setIsSubmitting(true);

    try {
      await crearReserva({
        user: DEFAULT_USER_ID,
        resource: Number(resource),
        date,
        start_time: startTime,
        end_time: endTime,
      });

      navigate("/");
    } catch (createError) {
      setSubmitError(
        createError instanceof Error
          ? createError.message
          : "No se pudo crear la reserva."
      );
    } finally {
      setIsSubmitting(false);
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

      {resourceError ? (
        <p className="status-text status-text--error">{resourceError}</p>
      ) : null}

      {submitError ? (
        <p className="status-text status-text--error">{submitError}</p>
      ) : null}

      <form onSubmit={handleSubmit} className="panel-card new-reservation-form">
        <div className="form-group">
          <label>Recurso</label>
          <select
            className="form-input"
            value={resource}
            onChange={(event) => setResource(event.target.value)}
            disabled={loadingResources || resources.length === 0}
          >
            <option value="">
              {loadingResources
                ? "Cargando recursos..."
                : resources.length === 0
                  ? "Sin recursos disponibles"
                  : "Selecciona un recurso"}
            </option>
            {resources.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
                {item.resource_type_name ? ` (${item.resource_type_name})` : ""}
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
            onChange={(event) => setDate(event.target.value)}
          />
        </div>

        <div className="time-grid">
          <div className="form-group">
            <label>Hora de inicio</label>
            <input
              className="form-input"
              type="time"
              value={startTime}
              onChange={(event) => setStartTime(event.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Hora de fin</label>
            <input
              className="form-input"
              type="time"
              value={endTime}
              onChange={(event) => setEndTime(event.target.value)}
            />
          </div>
        </div>

        <button
          type="submit"
          className="primary-button"
          disabled={isSubmitting || loadingResources || resources.length === 0}
        >
          {isSubmitting ? "Guardando..." : "Guardar reserva"}
        </button>
      </form>
    </section>
  );
}

export default NewReservationPage;
