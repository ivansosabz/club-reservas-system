import { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import ReservationItem from "../components/ReservationItem";
import { eliminarReserva, getReservas } from "../services/reservaService";
import type { Reserva } from "../types/reserva";

function ReservationsPage() {
  const location = useLocation();
  const [reservations, setReservations] = useState<Reserva[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
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

  const handleDelete = useCallback(async (id: number) => {
    setDeletingIds((prev) => new Set(prev).add(id));

    try {
      await eliminarReserva(id);
      setReservations((prev) => prev.filter((r) => r.id !== id));
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "No se pudo eliminar la reserva."
      );
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
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

      {successMessage ? (
        <p className="status-text status-text--success">{successMessage}</p>
      ) : null}

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
                onDelete={handleDelete}
                isDeleting={deletingIds.has(reservation.id)}
              />
            ))}
          </ul>
        )
      ) : null}
    </section>
  );
}

export default ReservationsPage;
