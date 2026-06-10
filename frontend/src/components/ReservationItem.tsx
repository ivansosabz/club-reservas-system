import type { Reserva } from "../types/reserva";
import "./ReservationItem.css";

function formatTime(value: string) {
  return value ? value.slice(0, 5) : "";
}

interface ReservationItemProps {
  reservation: Reserva;
  onEdit?: (reservation: Reserva) => void;
  onDelete?: (id: number) => void;
  isDeleting?: boolean;
}

function ReservationItem({ reservation, onEdit, onDelete, isDeleting = false }: ReservationItemProps) {
  const { resource_name, date, start_time, end_time, status } = reservation;

  return (
    <li className="reservation-card">
      <div>
        <h3 className="reservation-card__title">
          {resource_name || "Recurso sin asignar"}
        </h3>

        <div className="reservation-card__details">
          <p>
            <span>Fecha:</span> {date}
          </p>
          <p>
            <span>Hora:</span> {formatTime(start_time)} - {formatTime(end_time)}
          </p>
          <p>
            <span>Estado:</span> {status || "Pendiente"}
          </p>
        </div>
      </div>

      <div className="reservation-card__actions">
        {onEdit ? (
          <button
            className="app-button"
            type="button"
            onClick={() => onEdit(reservation)}
          >
            Editar
          </button>
        ) : null}
        {onDelete ? (
          <button
            className="app-button app-button--danger"
            type="button"
            disabled={isDeleting}
            onClick={() => onDelete(reservation.id)}
          >
            {isDeleting ? "Eliminando..." : "Eliminar"}
          </button>
        ) : null}
      </div>
    </li>
  );
}

export default ReservationItem;
