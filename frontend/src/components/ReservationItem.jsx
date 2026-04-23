import "./ReservationItem.css";

// El backend devuelve las reservas con este shape:
// {
//   id, user, user_username, resource, resource_name,
//   date, start_time, end_time, status, notes, ...
// }
// Acá mostramos los campos legibles — `resource_name` ya viene resuelto
// por el serializer, así no tenemos que hacer otra llamada para el nombre.

function ReservationItem({ reservation, onDelete }) {
  const {
    id,
    resource_name,
    date,
    start_time,
    end_time,
    status,
  } = reservation;

  // Mostramos HH:MM recortando los segundos que Django manda como "HH:MM:SS".
  const formatTime = (t) => (t ? t.slice(0, 5) : "");

  return (
    <li className="reservation-card">
      <div>
        <h3 className="reservation-card__title">{resource_name}</h3>

        <div className="reservation-card__details">
          <p>
            <span>Fecha:</span> {date}
          </p>
          <p>
            <span>Hora:</span> {formatTime(start_time)} - {formatTime(end_time)}
          </p>
          <p>
            <span>Estado:</span> {status}
          </p>
        </div>
      </div>

      <div className="reservation-card__actions">
        <button
          className="app-button app-button--danger"
          type="button"
          onClick={() => onDelete(id)}
        >
          Eliminar
        </button>
      </div>
    </li>
  );
}

export default ReservationItem;
