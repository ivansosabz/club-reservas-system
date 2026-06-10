import { useCallback, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import LoadingSkeleton from "../components/LoadingSkeleton";
import ReservationItem from "../components/ReservationItem";
import { useAsync } from "../hooks/useAsync";
import { eliminarReserva, getReservas } from "../services/reservaService";

function ReservationsPage() {
  const location = useLocation();
  const {
    data: reservations,
    loading,
    error,
    setData: setReservations,
  } = useAsync(getReservas, []);
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [successMessage, setSuccessMessage] = useState(
    (location.state as { successMessage?: string } | null)?.successMessage ?? ""
  );

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  const handleDelete = useCallback(async (id: number) => {
    setDeletingIds((prev) => new Set(prev).add(id));

    try {
      await eliminarReserva(id);

      setReservations(
        (reservations ?? []).filter((r) => r.id !== id)
      );
    } catch (deleteError) {
      console.error(deleteError);
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  }, [reservations, setReservations]);

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Agenda deportiva</p>
        <h1 className="page-title">Reservas</h1>
        <p className="page-description">
          Consulta los turnos activos y gestiona tus espacios del club.
        </p>
      </header>

      {loading ? <LoadingSkeleton count={3} /> : null}

      {successMessage ? (
        <p className="status-text status-text--success">{successMessage}</p>
      ) : null}

      {!loading && error ? (
        <p className="status-text status-text--error">{error}</p>
      ) : null}

      {!loading && !error && reservations && reservations.length > 0 ? (
        <ul className="reservations-list">
          {reservations.map((reservation) => (
            <ReservationItem
              key={reservation.id}
              reservation={reservation}
              onDelete={handleDelete}
              isDeleting={deletingIds.has(reservation.id)}
            />
          ))}
        </ul>
      ) : null}

      {!loading && !error && reservations && reservations.length === 0 ? (
        <div className="empty-state">
          <p className="empty-state-icon">[ ]</p>
          <p className="empty-state-title">Todavia no hay reservas</p>
          <p className="empty-state-description">
            Crea tu primera reserva para empezar a gestionar los espacios del club.
          </p>
          <Link to="/new" className="primary-button" style={{ textDecoration: "none", display: "inline-flex" }}>
            Nueva reserva
          </Link>
        </div>
      ) : null}
    </section>
  );
}

export default ReservationsPage;
