import { useState } from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import AboutPage from "./pages/AboutPage";
import NewReservationPage from "./pages/NewReservationPage";
import ReservationsPage from "./pages/ReservationsPage";
import "./App.css";

function App() {
  const [reservations, setReservations] = useState([]);

  return (
    <div className="app-shell">
      <div className="app-layout">
        <nav className="main-nav">
          <div className="brand-mark">Club Reservas</div>

          <div className="nav-links">
            <NavLink className="nav-link" to="/">
              Reservas
            </NavLink>
            <NavLink className="nav-link" to="/new">
              Nueva reserva
            </NavLink>
            <NavLink className="nav-link" to="/about">
              Acerca de
            </NavLink>
          </div>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <ReservationsPage
                reservations={reservations}
                setReservations={setReservations}
              />
            }
          />
          <Route path="/about" element={<AboutPage />} />
          <Route
            path="/new"
            element={
              <NewReservationPage
                reservations={reservations}
                setReservations={setReservations}
              />
            }
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
