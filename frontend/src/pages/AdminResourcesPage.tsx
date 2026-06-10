import { useState } from "react";
import { useAsync } from "../hooks/useAsync";
import Modal from "../components/Modal";
import {
  getRecursos,
  getTiposRecurso,
  crearRecurso,
  actualizarRecurso,
  eliminarRecurso,
} from "../services/recursoService";
import type { Recurso, CrearRecursoPayload } from "../types/recurso";
import "./AdminResourceTypesPage.css";

function AdminResourcesPage() {
  const {
    data: recursos,
    loading,
    error,
    refresh,
  } = useAsync(() => getRecursos(true), [], []);
  const { data: tipos } = useAsync(getTiposRecurso, [], []);

  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState<Recurso | null>(null);
  const [name, setName] = useState("");
  const [resourceType, setResourceType] = useState("");
  const [description, setDescription] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function openCreate() {
    setEditing(null);
    setName("");
    setResourceType("");
    setDescription("");
    setIsActive(true);
    setSubmitError("");
    setModalOpen(true);
  }

  function openEdit(r: Recurso) {
    setEditing(r);
    setName(r.name);
    setResourceType(String(r.resource_type));
    setDescription(r.description ?? "");
    setIsActive(r.is_active ?? true);
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
    if (!resourceType) {
      setSubmitError("Selecciona un tipo de recurso.");
      return;
    }

    setIsSubmitting(true);
    try {
      if (editing) {
        await actualizarRecurso(editing.id, {
          name: name.trim(),
          resource_type: Number(resourceType),
          description: description.trim() || undefined,
          is_active: isActive,
        });
      } else {
        await crearRecurso({
          name: name.trim(),
          resource_type: Number(resourceType),
          description: description.trim() || undefined,
          is_active: isActive,
        });
      }
      closeModal();
      refresh();
    } catch (err) {
      setSubmitError(
        err instanceof Error ? err.message : "Error al guardar."
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm("Eliminar este recurso?")) return;
    try {
      await eliminarRecurso(id);
      refresh();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al eliminar.");
    }
  }

  async function handleToggleActive(r: Recurso) {
    try {
      await actualizarRecurso(r.id, { is_active: !r.is_active });
      refresh();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Error al actualizar.");
    }
  }

  return (
    <section className="page page--wide">
      <header className="page-header">
        <p className="page-kicker">Administracion</p>
        <h1 className="page-title">Recursos</h1>
        <p className="page-description">
          Administra los recursos reservables del club.
        </p>
      </header>

      <div className="admin-toolbar">
        <button className="primary-button" onClick={openCreate}>
          + Agregar recurso
        </button>
      </div>

      {loading && <p className="status-text">Cargando...</p>}
      {error && <p className="status-text status-text--error">{error}</p>}

      {!loading && !error && recursos.length === 0 && (
        <div className="empty-state">
          <p className="empty-state-title">Sin recursos</p>
          <p className="empty-state-description">
            Crea el primer recurso reservable del club.
          </p>
        </div>
      )}

      {recursos.length > 0 && (
        <div className="admin-table-wrapper">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Tipo</th>
                <th>Descripcion</th>
                <th className="admin-cell-status">Estado</th>
                <th className="admin-table-actions">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {recursos.map((r) => (
                <tr key={r.id}>
                  <td className="admin-cell-name">{r.name}</td>
                  <td>
                    <span className="admin-badge admin-badge--active">
                      {r.resource_type_name ?? "-"}
                    </span>
                  </td>
                  <td className="admin-cell-desc">
                    {r.description || "-"}
                  </td>
                  <td>
                    <span
                      className={
                        r.is_active
                          ? "admin-badge admin-badge--active"
                          : "admin-badge admin-badge--inactive"
                      }
                    >
                      {r.is_active ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                  <td className="admin-cell-actions">
                    <button
                      className="app-button"
                      onClick={() => openEdit(r)}
                    >
                      Editar
                    </button>
                    <button
                      className="app-button"
                      onClick={() => handleToggleActive(r)}
                    >
                      {r.is_active ? "Desactivar" : "Activar"}
                    </button>
                    <button
                      className="app-button app-button--danger"
                      onClick={() => handleDelete(r.id)}
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

      <Modal
        open={modalOpen}
        title={editing ? "Editar recurso" : "Agregar recurso"}
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
            <label>Tipo de recurso</label>
            <select
              className="form-input"
              value={resourceType}
              onChange={(e) => setResourceType(e.target.value)}
            >
              <option value="">Selecciona un tipo</option>
              {tipos.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
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
          <div className="form-group">
            <label className="admin-toggle-label">
              <input
                type="checkbox"
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
                className="admin-toggle-checkbox"
              />
              Recurso activo
            </label>
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
                : "Crear recurso"}
          </button>
        </form>
      </Modal>
    </section>
  );
}

export default AdminResourcesPage;
