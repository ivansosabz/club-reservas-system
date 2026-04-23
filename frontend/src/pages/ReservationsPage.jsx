import { useEffect, useState } from "react";
import ReservationItem from "../components/ReservationItem";
import { getReservations } from "../services/reservationsService";

function ReservationsPage({ reservations, setReservations }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function loadReservations() {
      try {
        const data = await getReservations();
        if (!cancelled) setReservations(data);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadReservations();

    // Cleanup: evita setear estado si el componente se desmonta
    // antes de que responda el fetch.
    return () => {
      cancelled = true;
    };
    // Deps vacías: cargamos una sola vez al montar.
    // `setReservations` es estable (viene de useState en App).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleDelete(id) {
    // TODO: cuando el backend exponga DELETE /api/reservations/:id/
    // disparar la llamada antes de sacarlo del estado local.
    setReservations((prev) => prev.filter((r) => r.id !== id));
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

      {loading && <p className="status-text">Cargando reservas...</p>}
      {error && <p className="status-text">Error: {error}</p>}

      {!loading && !error && (
        <ul className="reservations-list">
          {reservations.length === 0 ? (
            <p className="status-text">Todavía no hay reservas.</p>
          ) : (
            reservations.map((reserva) => (
              <ReservationItem
                key={reserva.id}
                reservation={reserva}
                onDelete={handleDelete}
              />
            ))
          )}
        </ul>
      )}
    </section>
  );
}

export default ReservationsPage;
