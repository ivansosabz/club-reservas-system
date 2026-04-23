import { useEffect, useState } from "react";
import { getRecursos } from "../services/recursoService";
import { crearReserva } from "../services/reservaService";
import "./NewReservationPage.css";

function NewReservationPage() {
  const [recurso, setRecurso] = useState("");
  const [recursos, setRecursos] = useState([]);
  const [fecha, setFecha] = useState("");
  const [horaInicio, setHoraInicio] = useState("");
  const [horaFin, setHoraFin] = useState("");
  const [loadingRecursos, setLoadingRecursos] = useState(true);
  const [resourceError, setResourceError] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isActive = true;

    async function loadRecursos() {
      try {
        const data = await getRecursos();

        if (!isActive) {
          return;
        }

        setRecursos(data);
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
          setLoadingRecursos(false);
        }
      }
    }

    void loadRecursos();

    return () => {
      isActive = false;
    };
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitError("");
    setSuccessMessage("");

    if (!recurso || !fecha || !horaInicio || !horaFin) {
      setSubmitError("Completa todos los campos.");
      return;
    }

    if (horaInicio >= horaFin) {
      setSubmitError("La hora de inicio debe ser menor a la de fin.");
      return;
    }

    setIsSubmitting(true);

    try {
      await crearReserva({
        recurso: Number(recurso),
        fecha,
        hora_inicio: horaInicio,
        hora_fin: horaFin,
      });

      setRecurso("");
      setFecha("");
      setHoraInicio("");
      setHoraFin("");
      setSuccessMessage("Reserva creada correctamente.");
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

      {successMessage ? (
        <p className="status-text status-text--success">{successMessage}</p>
      ) : null}

      <form onSubmit={handleSubmit} className="panel-card new-reservation-form">
        <div className="form-group">
          <label>Recurso</label>
          <select
            className="form-input"
            value={recurso}
            onChange={(e) => setRecurso(e.target.value)}
            disabled={loadingRecursos || recursos.length === 0}
          >
            <option value="">
              {loadingRecursos
                ? "Cargando recursos..."
                : recursos.length === 0
                  ? "Sin recursos disponibles"
                  : "Selecciona un recurso"}
            </option>
            {recursos.map((item) => (
              <option key={item.id} value={item.id}>
                {item.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Fecha</label>
          <input
            className="form-input"
            type="date"
            value={fecha}
            onChange={(e) => setFecha(e.target.value)}
          />
        </div>

        <div className="time-grid">
          <div className="form-group">
            <label>Hora de inicio</label>
            <input
              className="form-input"
              type="time"
              value={horaInicio}
              onChange={(e) => setHoraInicio(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Hora de fin</label>
            <input
              className="form-input"
              type="time"
              value={horaFin}
              onChange={(e) => setHoraFin(e.target.value)}
            />
          </div>
        </div>

        <button
          type="submit"
          className="primary-button"
          disabled={isSubmitting || loadingRecursos || recursos.length === 0}
        >
          {isSubmitting ? "Guardando..." : "Guardar reserva"}
        </button>
      </form>
    </section>
  );
}

export default NewReservationPage;
