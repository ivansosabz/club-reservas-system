import { useEffect, useState } from "react";
import ReservationItem from "../components/ReservationItem";
import { getReservas } from "../services/reservaService";

function ReservationsPage() {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadReservations() {
      try {
        const data = await getReservas();

        if (cancelled) {
          return;
        }

        setReservations(data);
        setError("");
      } catch (loadError) {
        if (cancelled) {
          return;
        }

        setError(
          loadError instanceof Error
            ? loadError.message
            : "No se pudieron cargar las reservas."
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadReservations();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Agenda deportiva</p>
        <h1 className="page-title">Reservas</h1>
        <p className="page-description">
          Consulta los turnos activos y gestiona tus espacios del club.
        </p>
      </header>

      {loading ? <p className="status-text">Cargando reservas...</p> : null}

      {!loading && error ? (
        <p className="status-text status-text--error">{error}</p>
      ) : null}

      {!loading && !error ? (
        reservations.length === 0 ? (
          <p className="status-text">Todavia no hay reservas.</p>
        ) : (
          <ul className="reservations-list">
            {reservations.map((reservation) => (
              <ReservationItem
                key={reservation.id}
                reservation={reservation}
              />
            ))}
          </ul>
        )
      ) : null}
    </section>
  );
}

export default ReservationsPage;
