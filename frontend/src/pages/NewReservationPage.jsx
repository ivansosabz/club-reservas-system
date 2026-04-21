import { useState } from "react";
import "./NewReservationPage.css";

function NewReservationPage({ reservations, setReservations }) {
  const [recurso, setRecurso] = useState("");
  const [fecha, setFecha] = useState("");
  const [horaInicio, setHoraInicio] = useState("");
  const [horaFin, setHoraFin] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!recurso || !fecha || !horaInicio || !horaFin) {
      alert("Completá todos los campos");
      return;
    }

    if (horaInicio >= horaFin) {
      alert("La hora de inicio debe ser menor a la de fin");
      return;
    }

    const nuevaReserva = {
      id: Date.now(),
      recurso,
      fecha,
      hora: `${horaInicio} - ${horaFin}`,
    };

    setReservations([...reservations, nuevaReserva]);

    setRecurso("");
    setFecha("");
    setHoraInicio("");
    setHoraFin("");
  }

  return (
    <section className="new-reservation-page">
      <header className="page-header">
        <p className="page-kicker">Nuevo turno</p>
        <h1 className="page-title">Nueva reserva</h1>
        <p className="page-description">
          Completa los datos del recurso y define el horario de uso.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="panel-card new-reservation-form">
        <div className="form-group">
          <label>Recurso</label>
          <input
            className="form-input"
            type="text"
            value={recurso}
            onChange={(e) => setRecurso(e.target.value)}
            placeholder="Ej: Cancha 1"
          />
        </div>

        <div className="form-group">
          <label>Fecha</label>
          <input
            className="form-input"
            type="date"
            value={fecha}
            onChange={(e) => setFecha(e.target.value)}
          />
        </div>

        <div className="time-grid">
          <div className="form-group">
            <label>Hora de inicio</label>
            <input
              className="form-input"
              type="time"
              value={horaInicio}
              onChange={(e) => setHoraInicio(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Hora de fin</label>
            <input
              className="form-input"
              type="time"
              value={horaFin}
              onChange={(e) => setHoraFin(e.target.value)}
            />
          </div>
        </div>

        <button type="submit" className="primary-button">
          Guardar reserva
        </button>
      </form>
    </section>
  );
}

export default NewReservationPage;
