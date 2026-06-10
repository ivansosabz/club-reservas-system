import { useState } from "react";
import { useAsync } from "../hooks/useAsync";
import Modal from "../components/Modal";
import {
  getTiposRecurso,
  crearTipoRecurso,
  actualizarTipoRecurso,
  eliminarTipoRecurso,
} from "../services/recursoService";
import type { TipoRecurso, CrearTipoRecursoPayload } from "../types/recurso";
import "./AdminResourceTypesPage.css";

const PAGE_SIZE = 10;

function AdminResourceTypesPage() {
  const {
    data: tipos,
    loading,
    error,
    refresh,
  } = useAsync(getTiposRecurso, [], []);
  const [page, setPage] = useState(1);

  const start = (page - 1) * PAGE_SIZE;
  const visible = (tipos ?? []).slice(start, start + PAGE_SIZE);
  const totalPages = Math.ceil((tipos ?? []).length / PAGE_SIZE);

  function handleRefresh() {
    setPage(1);
    refresh();
  }

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<TipoRecurso | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function openCreate() {
    setEditing(null);
    setName("");
    setDescription("");
    setSubmitError("");
    setModalOpen(true);
  }

  function openEdit(tipo: TipoRecurso) {
    setEditing(tipo);
    setName(tipo.name);
    setDescription(tipo.description ?? "");
    setSubmitError("");
    setModalOpen(true);
  }

  function closeModal() {
    setModalOpen(false);
    setEditing(null);
    setSubmitError("");
  }

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setSubmitError("");

    if (!name.trim()) {
      setSubmitError("El nombre es obligatorio.");
      return;
    }

    setIsSubmitting(true);
    try {
      if (editing) {
        await actualizarTipoRecurso(editing.id, {
          name: name.trim(),
          description: description.trim() || undefined,
        } as CrearTipoRecursoPayload);
      } else {
        await crearTipoRecurso({
          name: name.trim(),
          description: description.trim() || undefined,
        });
      }
      closeModal();
      handleRefresh();
    } catch (err) {
      setSubmitError(
        err instanceof Error ? err.message : "Error al guardar."
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm("Eliminar este tipo de recurso?")) return;
    try {
      await eliminarTipoRecurso(id);
      handleRefresh();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al eliminar.");
    }
  }

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Administracion</p>
        <h1 className="page-title">Tipos de recurso</h1>
        <p className="page-description">
          Crea, edita y elimina los tipos de recurso del club.
        </p>
      </header>

      <div className="admin-toolbar">
        <button className="primary-button" onClick={openCreate}>
          + Agregar tipo
        </button>
      </div>

      {loading && <p className="status-text">Cargando...</p>}
      {error && <p className="status-text status-text--error">{error}</p>}

      {!loading && !error && tipos.length === 0 && (
        <div className="empty-state">
          <p className="empty-state-title">Sin tipos de recurso</p>
          <p className="empty-state-description">
            Crea el primer tipo para empezar a organizar los recursos.
          </p>
        </div>
      )}

      {tipos.length > 0 && (
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripcion</th>
                <th className="admin-table-actions">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {visible.map((tipo) => (
                <tr key={tipo.id}>
                  <td className="admin-cell-name">{tipo.name}</td>
                  <td className="admin-cell-desc">{tipo.description ?? "-"}</td>
                  <td className="admin-cell-actions">
                    <button
                      className="app-button"
                      onClick={() => openEdit(tipo)}
                    >
                      Editar
                    </button>
                    <button
                      className="app-button app-button--danger"
                      onClick={() => handleDelete(tipo.id)}
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {totalPages > 1 ? (
        <div className="pagination-bar">
          <button
            type="button"
            className="app-button"
            disabled={page <= 1}
            onClick={() => setPage(page - 1)}
          >
            Anterior
          </button>
          <span className="pagination-info">
            Pagina {page} de {totalPages} ({tipos.length} tipos)
          </span>
          <button
            type="button"
            className="app-button"
            disabled={page >= totalPages}
            onClick={() => setPage(page + 1)}
          >
            Siguiente
          </button>
        </div>
      ) : null}

      <Modal
        open={modalOpen}
        title={editing ? "Editar tipo" : "Agregar tipo"}
        onClose={closeModal}
      >
        <form onSubmit={handleSubmit}>
          {submitError && (
            <p className="status-text status-text--error">{submitError}</p>
          )}
          <div className="form-group">
            <label>Nombre</label>
            <input
              className="form-input"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoFocus
            />
          </div>
          <div className="form-group">
            <label>Descripcion</label>
            <textarea
              className="form-input form-textarea"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>
          <button
            type="submit"
            className="primary-button"
            style={{ width: "100%" }}
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Guardando..."
              : editing
                ? "Guardar cambios"
                : "Crear tipo"}
          </button>
        </form>
      </Modal>
    </section>
  );
}

export default AdminResourceTypesPage;
