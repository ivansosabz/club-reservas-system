import { useCallback, useEffect, useState } from "react";
import { Link, useLocation, useSearchParams } from "react-router-dom";
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
import type { ActualizarReservaPayload, Reserva, ReservaFilters } from "../types/reserva";
import Modal from "../components/Modal";
import "./ReservationsPage.css";

function ReservationsPage() {
  const location = useLocation();
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();

  const page = Number(searchParams.get("page") || "1");
  const pageSize = Number(searchParams.get("page_size") || "20");
  const dateFrom = searchParams.get("date_from") || "";
  const dateTo = searchParams.get("date_to") || "";
  const statusFilter = searchParams.get("status") || "";
  const resourceFilter = searchParams.get("resource") || "";
  const searchTerm = searchParams.get("search") || "";
  const ordering = searchParams.get("ordering") || "";

  const filters: ReservaFilters = {
    page,
    page_size: pageSize,
    ...(dateFrom ? { date_from: dateFrom } : {}),
    ...(dateTo ? { date_to: dateTo } : {}),
    ...(statusFilter ? { status: statusFilter } : {}),
    ...(resourceFilter ? { resource: Number(resourceFilter) } : {}),
    ...(searchTerm ? { search: searchTerm } : {}),
    ...(ordering ? { ordering } : {}),
  };

  const fetchKey = JSON.stringify(filters);

  const {
    data: paginated,
    loading,
    error,
    setData,
    refresh,
  } = useAsync(() => getReservas(filters), [fetchKey]);

  const { data: recursos } = useAsync(getRecursos, [], []);

  const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
  const [successMessage, setSuccessMessage] = useState(
    (location.state as { successMessage?: string } | null)?.successMessage ?? ""
  );

  const [editing, setEditing] = useState<Reserva | null>(null);
  const [editResource, setEditResource] = useState("");
  const [editStartDatetime, setEditStartDatetime] = useState("");
  const [editEndDatetime, setEditEndDatetime] = useState("");
  const [editStatus, setEditStatus] = useState("");
  const [editNotes, setEditNotes] = useState("");
  const [editError, setEditError] = useState("");
  const [isEditing, setIsEditing] = useState(false);

  const reservations = paginated?.results ?? [];
  const totalCount = paginated?.count ?? 0;
  const totalPages = Math.ceil(totalCount / pageSize);

  useEffect(() => {
    if (successMessage) {
      const timer = setTimeout(() => setSuccessMessage(""), 3000);
      return () => clearTimeout(timer);
    }
  }, [successMessage]);

  function setFilter(key: string, value: string) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (value) {
        next.set(key, value);
      } else {
        next.delete(key);
      }
      if (key !== "page") {
        next.delete("page");
      }
      return next;
    });
  }

  function clearFilters() {
    setSearchParams(new URLSearchParams());
  }

  function goToPage(p: number) {
    if (p < 1 || p > totalPages) return;
    setFilter("page", String(p));
  }

  const hasFilters = dateFrom || dateTo || statusFilter || resourceFilter || searchTerm;

  function openEdit(reservation: Reserva) {
    setEditing(reservation);
    setEditResource(String(reservation.resource));
    setEditStartDatetime(reservation.start_datetime.slice(0, 16));
    setEditEndDatetime(reservation.end_datetime.slice(0, 16));
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

    if (!editResource || !editStartDatetime || !editEndDatetime) {
      setEditError("Completa todos los campos obligatorios.");
      return;
    }
    if (editStartDatetime >= editEndDatetime) {
      setEditError("La fecha/hora de fin debe ser posterior a la de inicio.");
      return;
    }

    setIsEditing(true);
    try {
      const payload: ActualizarReservaPayload = {
        resource: Number(editResource),
        start_datetime: editStartDatetime + ":00",
        end_datetime: editEndDatetime + ":00",
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
      setData((prev) => {
        if (!prev) return prev;
        return {
          ...prev,
          count: prev.count - 1,
          results: prev.results.filter((r) => r.id !== id),
        };
      });
    } catch (deleteError) {
      console.error(deleteError);
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  }, [setData]);

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Agenda deportiva</p>
        <h1 className="page-title">Reservas</h1>
        <p className="page-description">
          Consulta los turnos activos y gestiona tus espacios del club.
        </p>
      </header>

      <div className="reservations-filters">
        <input
          className="form-input filter-search"
          type="search"
          placeholder="Buscar por recurso o usuario..."
          value={searchTerm}
          onChange={(e) => setFilter("search", e.target.value)}
        />
        <input
          className="form-input"
          type="date"
          value={dateFrom}
          onChange={(e) => setFilter("date_from", e.target.value)}
          title="Fecha desde"
        />
        <input
          className="form-input"
          type="date"
          value={dateTo}
          onChange={(e) => setFilter("date_to", e.target.value)}
          title="Fecha hasta"
        />
        <select
          className="form-input"
          value={statusFilter}
          onChange={(e) => setFilter("status", e.target.value)}
        >
          <option value="">Todos los estados</option>
          <option value="pending">Pendiente</option>
          <option value="confirmed">Confirmada</option>
          <option value="cancelled">Cancelada</option>
        </select>
        {hasFilters ? (
          <button
            type="button"
            className="app-button"
            onClick={clearFilters}
          >
            Limpiar filtros
          </button>
        ) : null}
      </div>

      {loading ? <LoadingSkeleton count={3} /> : null}

      {successMessage ? (
        <p className="status-text status-text--success">{successMessage}</p>
      ) : null}

      {!loading && error ? (
        <p className="status-text status-text--error">{error}</p>
      ) : null}

      {!loading && !error && reservations.length > 0 ? (
        <>
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

          {totalPages > 1 ? (
            <div className="pagination-bar">
              <button
                type="button"
                className="app-button"
                disabled={page <= 1}
                onClick={() => goToPage(page - 1)}
              >
                Anterior
              </button>
              <span className="pagination-info">
                Pagina {page} de {totalPages} ({totalCount} reservas)
              </span>
              <button
                type="button"
                className="app-button"
                disabled={page >= totalPages}
                onClick={() => goToPage(page + 1)}
              >
                Siguiente
              </button>
            </div>
          ) : null}
        </>
      ) : null}

      {!loading && !error && reservations.length === 0 ? (
        <div className="empty-state">
          <p className="empty-state-icon">[ ]</p>
          <p className="empty-state-title">
            {hasFilters ? "Sin resultados" : "Todavia no hay reservas"}
          </p>
          <p className="empty-state-description">
            {hasFilters
              ? "No se encontraron reservas con los filtros aplicados."
              : "Crea tu primera reserva para empezar a gestionar los espacios del club."
            }
          </p>
          {hasFilters ? (
            <button
              type="button"
              className="primary-button"
              onClick={clearFilters}
            >
              Limpiar filtros
            </button>
          ) : (
            <Link
              to="/new"
              className="primary-button"
              style={{ textDecoration: "none", display: "inline-flex" }}
            >
              Nueva reserva
            </Link>
          )}
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
              {recursos?.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                  {r.resource_type_name ? ` (${r.resource_type_name})` : ""}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Inicio</label>
            <input
              className="form-input"
              type="datetime-local"
              value={editStartDatetime}
              onChange={(e) => setEditStartDatetime(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Fin</label>
            <input
              className="form-input"
              type="datetime-local"
              value={editEndDatetime}
              min={editStartDatetime || undefined}
              onChange={(e) => setEditEndDatetime(e.target.value)}
            />
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
