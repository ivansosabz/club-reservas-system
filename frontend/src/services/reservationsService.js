export function getReservations() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          id: 1,
          recurso: "Cancha 1",
          fecha: "2026-04-21",
          hora: "18:00 - 19:00",
        },
        {
          id: 2,
          recurso: "Salón A",
          fecha: "2026-04-22",
          hora: "20:00 - 22:00",
        },
      ]);
    }, 1000);
  });
}