// Basic Service Worker for PWA Install Prompt
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Network first strategy to prevent breaking the live site
  event.respondWith(fetch(event.request));
});
