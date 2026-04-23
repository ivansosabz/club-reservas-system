import { useEffect, useState } from "react";
import ReservationItem from "../components/ReservationItem";
import { getRecursos } from "../services/recursoService";
import { eliminarReserva, getReservas } from "../services/reservaService";

function getResourceName(recurso, recursosMap) {
  if (typeof recurso === "string") {
    return recurso;
  }

  if (typeof recurso === "number") {
    return recursosMap.get(recurso) || `Recurso #${recurso}`;
  }

  if (recurso && typeof recurso === "object") {
    if (typeof recurso.nombre === "string") {
      return recurso.nombre;
    }

    if (typeof recurso.id === "number") {
      return recursosMap.get(recurso.id) || `Recurso #${recurso.id}`;
    }
  }

  return "Recurso sin asignar";
}

function formatReservation(reserva, recursosMap) {
  return {
    id: reserva.id,
    recurso: getResourceName(reserva.recurso, recursosMap),
    fecha: reserva.fecha,
    hora: `${reserva.hora_inicio} - ${reserva.hora_fin}`,
  };
}

async function fetchReservations() {
  const [reservasData, recursosData] = await Promise.all([
    getReservas(),
    getRecursos().catch(() => []),
  ]);

  const recursosMap = new Map(
    recursosData.map((recurso) => [recurso.id, recurso.nombre])
  );

  return reservasData.map((reserva) => formatReservation(reserva, recursosMap));
}

function ReservationsPage() {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    let isActive = true;

    async function loadReservations() {
      try {
        const data = await fetchReservations();

        if (!isActive) {
          return;
        }

        setReservations(data);
        setError("");
      } catch (loadError) {
        if (!isActive) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "No se pudieron cargar las reservas."
        );
      } finally {
        if (isActive) {
          setLoading(false);
        }
      }
    }

    void loadReservations();

    return () => {
      isActive = false;
    };
  }, []);

  async function handleDelete(id) {
    setDeletingId(id);
    setError("");

    try {
      await eliminarReserva(id);
      const data = await fetchReservations();
      setReservations(data);
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "No se pudo eliminar la reserva."
      );
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Agenda deportiva</p>
        <h1 className="page-title">Reservas</h1>
        <p className="page-description">
          Consulta los turnos activos y gestiona tus espacios del club.
        </p>
      </header>

      {error ? <p className="status-text status-text--error">{error}</p> : null}

      {loading ? (
        <p className="status-text">Cargando reservas...</p>
      ) : reservations.length === 0 ? (
        <p className="status-text">No hay reservas registradas.</p>
      ) : (
        <ul className="reservations-list">
          {reservations.map((reserva) => (
            <ReservationItem
              key={reserva.id}
              reservation={reserva}
              onDelete={handleDelete}
              isDeleting={deletingId === reserva.id}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

export default ReservationsPage;
