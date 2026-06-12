// Minimaler Service Worker für die App-Installierbarkeit.
// Bewusst KEIN Caching: das Tool lebt von Live-Daten (Resultate, Torschützen).
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', () => {});
