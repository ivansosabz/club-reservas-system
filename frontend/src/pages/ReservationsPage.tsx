import { useCallback, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import LoadingSkeleton from "../components/LoadingSkeleton";
import ReservationItem from "../components/ReservationItem";
import { useAsync } from "../hooks/useAsync";
import { useAuth } from "../contexts/AuthContext";
import { getRecursos } from "../services/recursoService";
import {
  actualizarReserva,
  eliminarReserva,
  getReservas,
} from "../services/reservaService";
import type { ActualizarReservaPayload, Reserva } from "../types/reserva";
import Modal from "../components/Modal";

function ReservationsPage() {
  const location = useLocation();
  const { user } = useAuth();
  const {
    data: reservations,
    loading,
    error,
    setData: setReservations,
    refresh,
  } = useAsync(getReservas, []);
  const { data: recursos } = useAsync(getRecursos, [], []);
  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [successMessage, setSuccessMessage] = useState(
    (location.state as { successMessage?: string } | null)?.successMessage ?? ""
  );

  const [editing, setEditing] = useState<Reserva | null>(null);
  const [editResource, setEditResource] = useState("");
  const [editDate, setEditDate] = useState("");
  const [editStartTime, setEditStartTime] = useState("");
  const [editEndTime, setEditEndTime] = useState("");
  const [editStatus, setEditStatus] = useState("");
  const [editNotes, setEditNotes] = useState("");
  const [editError, setEditError] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  function openEdit(reservation: Reserva) {
    setEditing(reservation);
    setEditResource(String(reservation.resource));
    setEditDate(reservation.date);
    setEditStartTime(reservation.start_time.slice(0, 5));
    setEditEndTime(reservation.end_time.slice(0, 5));
    setEditStatus(reservation.status ?? "pending");
    setEditNotes(reservation.notes ?? "");
    setEditError("");
    setIsEditing(false);
  }

  function closeEdit() {
    setEditing(null);
    setEditError("");
  }

  async function handleEditSubmit(event: React.FormEvent) {
    event.preventDefault();
    setEditError("");

    if (!editResource || !editDate || !editStartTime || !editEndTime) {
      setEditError("Completa todos los campos obligatorios.");
      return;
    }
    if (editStartTime >= editEndTime) {
      setEditError("La hora de inicio debe ser menor a la de fin.");
      return;
    }

    setIsEditing(true);
    try {
      const payload: ActualizarReservaPayload = {
        resource: Number(editResource),
        date: editDate,
        start_time: editStartTime,
        end_time: editEndTime,
        status: editStatus,
        notes: editNotes || undefined,
      };
      await actualizarReserva(editing!.id, payload);
      closeEdit();
      refresh();
      setSuccessMessage("Reserva actualizada con exito");
    } catch (err) {
      setEditError(
        err instanceof Error ? err.message : "Error al actualizar."
      );
    } finally {
      setIsEditing(false);
    }
  }

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
              onEdit={user?.is_staff ? openEdit : undefined}
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

      <Modal
        open={editing !== null}
        title="Editar reserva"
        onClose={closeEdit}
      >
        <form onSubmit={handleEditSubmit}>
          {editError ? (
            <p className="status-text status-text--error">{editError}</p>
          ) : null}
          <div className="form-group">
            <label>Recurso</label>
            <select
              className="form-input"
              value={editResource}
              onChange={(e) => setEditResource(e.target.value)}
            >
              {recursos.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                  {r.resource_type_name ? ` (${r.resource_type_name})` : ""}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Fecha</label>
            <input
              className="form-input"
              type="date"
              value={editDate}
              onChange={(e) => setEditDate(e.target.value)}
            />
          </div>
          <div className="time-grid">
            <div className="form-group">
              <label>Hora inicio</label>
              <input
                className="form-input"
                type="time"
                value={editStartTime}
                onChange={(e) => setEditStartTime(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Hora fin</label>
              <input
                className="form-input"
                type="time"
                value={editEndTime}
                onChange={(e) => setEditEndTime(e.target.value)}
              />
            </div>
          </div>
          <div className="form-group">
            <label>Estado</label>
            <select
              className="form-input"
              value={editStatus}
              onChange={(e) => setEditStatus(e.target.value)}
            >
              <option value="pending">Pendiente</option>
              <option value="confirmed">Confirmada</option>
              <option value="cancelled">Cancelada</option>
            </select>
          </div>
          <div className="form-group">
            <label>Notas</label>
            <textarea
              className="form-input form-textarea"
              value={editNotes}
              onChange={(e) => setEditNotes(e.target.value)}
              rows={3}
            />
          </div>
          <button
            type="submit"
            className="primary-button"
            disabled={isEditing}
          >
            {isEditing ? "Guardando..." : "Guardar cambios"}
          </button>
        </form>
      </Modal>
    </section>
  );
}

export default ReservationsPage;
