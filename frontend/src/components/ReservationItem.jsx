import "./ReservationItem.css";

function formatTime(value) {
  return value ? value.slice(0, 5) : "";
}

function ReservationItem({ reservation, onDelete, isDeleting = false }) {
  const { id, resource_name, date, start_time, end_time, status } = reservation;

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

      {onDelete ? (
        <div className="reservation-card__actions">
          <button
            className="app-button app-button--danger"
            type="button"
            disabled={isDeleting}
            onClick={() => onDelete(id)}
          >
            {isDeleting ? "Eliminando..." : "Eliminar"}
          </button>
        </div>
      ) : null}
    </li>
  );
}

export default ReservationItem;
