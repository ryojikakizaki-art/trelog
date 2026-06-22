var C = 'trelog-v38';
var ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './snd-warn.mp3', './snd-go.mp3'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(C).then(function (c) { return c.addAll(ASSETS); }));
  self.skipWaiting();
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.map(function (k) { if (k !== C) return caches.delete(k); }));
  }));
  self.clients.claim();
});
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(function (r) {
      return r || fetch(e.request).catch(function () { return caches.match('./index.html'); });
    })
  );
});
self.addEventListener('push', function (e) {
  e.waitUntil(self.registration.showNotification('休憩おわり！', {
    body: '次のセットへ', tag: 'rest', renotify: true, vibrate: [300, 120, 300], requireInteraction: false
  }));
});
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: 'window' }).then(function (cs) {
    for (var i = 0; i < cs.length; i++) { if ('focus' in cs[i]) return cs[i].focus(); }
    if (self.clients.openWindow) return self.clients.openWindow('./');
  }));
});
