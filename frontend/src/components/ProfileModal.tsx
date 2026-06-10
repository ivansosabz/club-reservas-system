import { useEffect, useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import Modal from "./Modal";

interface ProfileModalProps {
  open: boolean;
  onClose: () => void;
}

function ProfileModal({ open, onClose }: ProfileModalProps) {
  const { user, updateProfile } = useAuth();
  const [editing, setEditing] = useState(false);
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (open) {
      setEmail(user?.email ?? "");
      setPhone(user?.phone ?? "");
      setError("");
      setEditing(false);
    }
  }, [open, user]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setSaving(true);
    try {
      await updateProfile({ email, phone: phone || null });
      setEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Modal open={open} title="Mi perfil" onClose={onClose}>
      {error ? (
        <p className="status-text status-text--error">{error}</p>
      ) : null}

      {editing ? (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Usuario</label>
            <input
              className="form-input"
              value={user?.username ?? ""}
              disabled
            />
          </div>
          <div className="form-group">
            <label>Email</label>
            <input
              className="form-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Telefono</label>
            <input
              className="form-input"
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+595 XXX XXX XXX"
            />
          </div>
          <div style={{ display: "flex", gap: 8 }}>
            <button
              type="submit"
              className="primary-button"
              disabled={saving}
            >
              {saving ? "Guardando..." : "Guardar cambios"}
            </button>
            <button
              type="button"
              className="app-button"
              onClick={() => {
                setEmail(user?.email ?? "");
                setPhone(user?.phone ?? "");
                setError("");
                setEditing(false);
              }}
            >
              Cancelar
            </button>
          </div>
        </form>
      ) : (
        <>
          <div className="form-group">
            <label>Usuario</label>
            <p className="profile-value">{user?.username ?? "-"}</p>
          </div>
          <div className="form-group">
            <label>Email</label>
            <p className="profile-value">{user?.email || "-"}</p>
          </div>
          <div className="form-group">
            <label>Telefono</label>
            <p className="profile-value">{user?.phone || "-"}</p>
          </div>
          <button
            type="button"
            className="primary-button"
            onClick={() => setEditing(true)}
          >
            Editar
          </button>
        </>
      )}
    </Modal>
  );
}

export default ProfileModal;
