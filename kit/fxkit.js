// Shared helpers for the effect scenes. Needs window.TRACK (assets/tracking.js from prep.py) and GSAP.
// Each effect sets window.FX_START (seconds into plate.mp4 where the scene starts) before loading this file.
window.FX = (function () {
  const T = window.TRACK || { fps: 30, frames: 1, width: 1080, height: 1920, face: [{ cx: 540, cy: 600, w: 300, h: 380, forehead: [540, 420], leye: [480, 560], reye: [600, 560], chin: [540, 800], tilt: 0 }], hands: [[null, null]] };
  const W = T.width, H = T.height;
  const idx = (t) => Math.max(0, Math.min(T.frames - 1, Math.round(((window.FX_START || 0) + t) * T.fps)));
  const face = (t) => T.face[idx(t)];
  const hands = (t) => T.hands[idx(t)] || [null, null];
  // calls cb(t) on every frame of [at, at + dur), seek-safe (driven by the paused timeline)
  function follow(tl, at, dur, cb) {
    const o = { v: 0 };
    tl.to(o, { v: 1, duration: dur, ease: 'none', onUpdate() { cb(at + this.time()); }, onStart() { cb(at); } }, at);
    cb(at);
  }
  // seeded random so every render is the same
  function rng(seed) {
    let a = seed >>> 0;
    return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  // type text into el, one character per `cps`
  function type(tl, el, text, at, cps = 22) {
    const o = { n: 0 };
    el.textContent = '';
    tl.to(o, { n: text.length, duration: text.length / cps, ease: 'none', onUpdate() { el.textContent = text.slice(0, Math.round(o.n)); } }, at);
  }
  // count a number up, keeping a suffix like K or %
  function count(tl, el, from, to, at, dur, fmt = (v) => Math.round(v)) {
    const o = { v: from };
    el.textContent = fmt(from);
    tl.to(o, { v: to, duration: dur, ease: 'power2.out', onUpdate() { el.textContent = fmt(o.v); } }, at);
  }
  const palm = (h) => { const k = [0, 5, 9, 13, 17]; return [k.reduce((s, i) => s + h.pts[i][0], 0) / 5, k.reduce((s, i) => s + h.pts[i][1], 0) / 5]; };
  return { T, W, H, idx, face, hands, follow, rng, type, count, palm };
})();
