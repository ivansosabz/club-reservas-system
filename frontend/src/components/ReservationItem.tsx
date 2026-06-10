import type { Reserva } from "../types/reserva";
import "./ReservationItem.css";

function fmt(dt: string) {
  const d = dt.slice(0, 10);
  const t = dt.slice(11, 16);
  return { date: d, time: t };
}

function statusLabel(s?: string) {
  switch (s) {
    case "confirmed":
      return "Confirmada";
    case "cancelled":
      return "Cancelada";
    default:
      return "Pendiente";
  }
}

interface ReservationItemProps {
  reservation: Reserva;
  onClick?: (reservation: Reserva) => void;
}

function ReservationItem({ reservation, onClick }: ReservationItemProps) {
  const { resource_name, start_datetime, end_datetime, status, user_phone, user_username } = reservation;
  const start = fmt(start_datetime);
  const end = fmt(end_datetime);
  const isMultiDay = start.date !== end.date;
  const label = statusLabel(status);

  return (
    <li
      className={`reservation-card${onClick ? " reservation-card--clickable" : ""}`}
      onClick={() => onClick?.(reservation)}
    >
      <div className="reservation-card__header">
        <h3 className="reservation-card__title">
          {resource_name || "Recurso sin asignar"}
        </h3>
        <span className={`reservation-card__badge reservation-card__badge--${status || "pending"}`}>
          {label}
        </span>
      </div>

      <div className="reservation-card__body">
        <div className="reservation-card__details">
          <div className="reservation-card__detail">
            <span className="reservation-card__label">Fecha</span>
            <span>{isMultiDay ? `${start.date} a ${end.date}` : start.date}</span>
          </div>
          <div className="reservation-card__detail">
            <span className="reservation-card__label">Hora</span>
            <span>{start.time} - {end.time}</span>
          </div>
          {user_username ? (
            <div className="reservation-card__detail">
              <span className="reservation-card__label">Usuario</span>
              <span>{user_username}</span>
            </div>
          ) : null}
          {user_phone ? (
            <div className="reservation-card__detail">
              <span className="reservation-card__label">Tel</span>
              <span>{user_phone}</span>
            </div>
          ) : null}
        </div>
      </div>
    </li>
  );
}

export default ReservationItem;