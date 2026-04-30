function AboutPage() {
  return (
    <section className="page">
      <header className="page-header">
        <p className="page-kicker">Club Reservas</p>
        <h1 className="page-title">Acerca del sistema</h1>
        <p className="page-description">
          Una interfaz simple para organizar espacios deportivos, horarios y
          reservas del club en un mismo lugar.
        </p>
      </header>

      <div className="about-grid">
        <article className="panel-card about-card">
          <h3>Gestion deportiva</h3>
          <p>
            Consulta turnos disponibles, registra nuevas reservas y mantene una
            agenda clara para canchas, salones y recursos compartidos.
          </p>
        </article>

        <article className="panel-card about-card">
          <h3>Interfaz consistente</h3>
          <p>
            El diseño usa cards, botones y espaciados comunes para que cada
            vista se sienta parte del mismo sistema.
          </p>
        </article>
      </div>
    </section>
  );
}

export default AboutPage;
