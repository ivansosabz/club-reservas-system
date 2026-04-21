import { useEffect, useState } from "react";
import ReservationItem from "../components/ReservationItem";
import { getReservations } from "../services/reservationsService";

function ReservationsPage({ reservations, setReservations }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReservations() {
      if (reservations.length === 0) {
        const data = await getReservations();
        setReservations(data);
      }

      setLoading(false);
    }

    loadReservations();
  }, [reservations, setReservations]);

  function handleDelete(id) {
    setReservations((prev) =>
      prev.filter((reservation) => reservation.id !== id)
    );
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

      {loading ? (
        <p className="status-text">Cargando reservas...</p>
      ) : (
        <ul className="reservations-list">
          {reservations.map((reserva) => (
            <ReservationItem
              key={reserva.id}
              reservation={reserva}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

export default ReservationsPage;
