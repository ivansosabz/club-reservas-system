# Club Reservas System

Sistema web para la gestión de reservas de instalaciones de un club (canchas, salones y similares). Diseñado para manejar solicitudes concurrentes y evitar conflictos de horarios.

## Tech Stack

- **Backend:** Django REST Framework (Python)
- **Frontend:** React
- **Base de datos:** PostgreSQL

---

## Estructura del proyecto

```
club-reservas-system/
├── backend/
├── frontend/
├── docs/
└── README.md
```

---

## Objetivo

Implementar un sistema de reservas concurrente que garantice la integridad de los horarios y gestione múltiples solicitudes simultáneas sin conflictos.

---

## Flujo de trabajo con Git

Repositorio único compartido (sin forks) con la siguiente estrategia de ramas:

| Rama | Propósito |
|------|-----------|
| `main` | Versión estable — se toca solo cuando hay algo funcional y cerrado |
| `feature/*` | Desarrollo de nuevas funcionalidades |

> **Nota:** Estamos en fase de desarrollo activo. Todo el trabajo ocurre en ramas `feature/*`. Los merges a `main` se reservan para hitos concretos (módulo completo, MVP, entrega).

### Paso a paso

```bash
# 1. Partir siempre desde main actualizado
git checkout main
git pull

# 2. Crear rama para la feature
git checkout -b feature/nombre-descriptivo

# 3. Trabajar, commitear y subir
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-descriptivo

# 4. Abrir Pull Request hacia main en GitHub
# 5. Esperar revisión antes del merge
```

### Convención de commits

```
feat:      nueva funcionalidad
fix:       corrección de errores
refactor:  mejora interna sin cambio de comportamiento
docs:      cambios en documentación
```

### Protección de ramas

La rama `main` tiene activada la protección en GitHub (Branch protection rules), lo que impide push directo. Todo cambio entra únicamente por Pull Request revisado por el equipo.

---

## Equipo

Proyecto desarrollado por un equipo de 3 integrantes con metodología real de desarrollo colaborativo.
