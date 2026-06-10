import type { Reserva } from "../types/reserva";
import "./ReservationItem.css";

function fmt(dt: string) {
  const d = dt.slice(0, 10);
  const t = dt.slice(11, 16);
  return { date: d, time: t };
}

interface ReservationItemProps {
  reservation: Reserva;
  onEdit?: (reservation: Reserva) => void;
  onDelete?: (id: number) => void;
  isDeleting?: boolean;
}

function ReservationItem({ reservation, onEdit, onDelete, isDeleting = false }: ReservationItemProps) {
  const { resource_name, start_datetime, end_datetime, status } = reservation;
  const start = fmt(start_datetime);
  const end = fmt(end_datetime);
  const isMultiDay = start.date !== end.date;

  return (
    <li className="reservation-card">
      <div>
        <h3 className="reservation-card__title">
          {resource_name || "Recurso sin asignar"}
        </h3>

        <div className="reservation-card__details">
          <p>
            <span>Fecha:</span> {isMultiDay ? `${start.date} a ${end.date}` : start.date}
          </p>
          <p>
            <span>Hora:</span> {start.time} - {end.time}
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
