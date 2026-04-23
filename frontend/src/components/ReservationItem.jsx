import "./ReservationItem.css";

function ReservationItem({ reservation, onDelete, isDeleting = false }) {
  const { recurso, fecha, hora } = reservation;

  return (
    <li className="reservation-card">
      <div>
        <h3 className="reservation-card__title">{recurso}</h3>

        <div className="reservation-card__details">
          <p>
            <span>Fecha:</span> {fecha}
          </p>
          <p>
            <span>Hora:</span> {hora}
          </p>
        </div>
      </div>

      <div className="reservation-card__actions">
        <button
          className="app-button app-button--danger"
          type="button"
          disabled={isDeleting}
          onClick={() => onDelete(reservation.id)}
        >
          {isDeleting ? "Eliminando..." : "Eliminar"}
        </button>
      </div>
    </li>
  );
}

export default ReservationItem;
