import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { useAsync } from "../hooks/useAsync";
import { getRecursos } from "../services/recursoService";
import { crearReserva } from "../services/reservaService";
import type { CrearReservaPayload } from "../types/reserva";
import "./NewReservationPage.css";

function NewReservationPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [resource, setResource] = useState("");
  const [startDatetime, setStartDatetime] = useState("");
  const [endDatetime, setEndDatetime] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    data: resources,
    loading: loadingResources,
    error: resourceError,
  } = useAsync(getRecursos, [], []);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitError("");

    if (!resource || !startDatetime || !endDatetime) {
      setSubmitError("Completa todos los campos.");
      return;
    }

    if (startDatetime >= endDatetime) {
      setSubmitError("La fecha/hora de fin debe ser posterior a la de inicio.");
      return;
    }

    setIsSubmitting(true);

    try {
      const payload: CrearReservaPayload = {
        user: user!.id,
        resource: Number(resource),
        start_datetime: startDatetime + ":00",
        end_datetime: endDatetime + ":00",
      };

      await crearReserva(payload);

      navigate("/", { state: { successMessage: "Reserva creada con éxito" } });
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
    <section className="page new-reservation-page">
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
          <label>Inicio</label>
          <input
            className="form-input"
            type="datetime-local"
            value={startDatetime}
            onChange={(event) => setStartDatetime(event.target.value)}
          />
        </div>

        <div className="form-group">
          <label>Fin</label>
          <input
            className="form-input"
            type="datetime-local"
            value={endDatetime}
            min={startDatetime || undefined}
            onChange={(event) => setEndDatetime(event.target.value)}
          />
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
