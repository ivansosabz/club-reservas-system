import { NavLink, Route, Routes } from "react-router-dom";
import AboutPage from "./pages/AboutPage";
import NewReservationPage from "./pages/NewReservationPage";
import ReservationsPage from "./pages/ReservationsPage";
import "./App.css";

function App() {
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
          <Route path="/" element={<ReservationsPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/new" element={<NewReservationPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
