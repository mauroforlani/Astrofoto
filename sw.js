const CACHE = 'astrofoto-v3';
const SHELL = [
  '/Astrofoto/',
  '/Astrofoto/index.html'
];

// Install: cache only the app shell
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

// Activate: delete old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = e.request.url;

  // Always network-first: API calls, data.json, images
  const alwaysNetwork = (
    url.includes('api.open-meteo.com') ||
    url.includes('nominatim.openstreetmap.org') ||
    url.includes('api.github.com') ||
    url.includes('data.json') ||
    url.includes('/img/')
  );

  if (alwaysNetwork) {
    e.respondWith(
      fetch(e.request).catch(() => new Response('', { status: 503 }))
    );
    return;
  }

  // Cache-first for app shell (index.html, manifest, sw.js)
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      });
    })
  );
});
