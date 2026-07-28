// frontend/public/sw.js
// AegisOps Enterprise PWA Service Worker for Offline Resilience

const CACHE_NAME = "aegisops-v1";
const ASSETS_TO_CACHE = [
  "/",
  "/index.html",
  "/src/main.tsx",
  "/src/App.tsx",
  "/src/index.css"
];

// Install Event
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("[Service Worker] Caching static shell assets");
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Activate Event
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("[Service Worker] Removing old cache", key);
            return caches.delete(key);
          }
        })
      );
    })
  );
});

// Fetch Interceptor: Cache-First for static assets, Network-First for API calls
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  
  // API requests -> Network First
  if (url.pathname.includes("/api/v1/")) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Clone and cache the API response if successful
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // If network fails, serve from cache
          console.log("[Service Worker] Offline! Serving API from cache:", url.pathname);
          return caches.match(event.request);
        })
    );
  } else {
    // Static assets -> Cache First with Network fallback
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request);
      })
    );
  }
});
