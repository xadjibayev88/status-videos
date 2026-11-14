// Pet Rock (apex_wealths): shot timeline locked to the Uzbek voice (words.json from tools/voice/make_voice.py).
import WORDS from "./words.json";

export const FPS = 30;
export type V3 = [number, number, number];
export type Light = "day" | "golden";

const words = WORDS as { w: string; t0: number; t1: number }[];
/** frame where word #i starts */
export const W = (i: number) => Math.round(words[i].t0 * FPS);
export const TOTAL = Math.round((words[words.length - 1].t1 + 1.6) * FPS);

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * u * (u * (u * 6 - 15) + 10); };
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const lerp3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
export const span = (f: number, a: number, b: number) => clamp01((f - a) / Math.max(1, b - a));

export type Cam = { pos: V3; look: V3; fov: number; roll?: number };
export type Shot = { id: string; a: number; light: Light; cam: (f: number, u: number) => Cam };

/** slow push toward the look point: every hold creeps (0.15–0.35 %/frame) */
const push = (from: V3, look: V3, fov: number, amount = 0.12, roll = 0) => (_f: number, u: number): Cam => ({
  pos: lerp3(from, lerp3(from, look, amount), u), look, fov, roll,
});
const glide = (p0: V3, p1: V3, l0: V3, l1: V3, fov: number, roll = 0) => (_f: number, u: number): Cam => {
  const s = smooth(u);
  return { pos: lerp3(p0, p1, s), look: lerp3(l0, l1, s), fov, roll };
};

// key places (see world.ts)
export const TABLE: V3 = [0, 0.9, 1.6];
export const ROCK: V3 = [-0.05, 1.03, 1.6];
export const BOX: V3 = [0.42, 0.9, 1.6];
export const GARY: V3 = [-0.95, 0, 1.75];

export const SHOTS: Shot[] = [
  { id: "hook", a: 0, light: "day", cam: push([0.55, 1.42, 3.05], [-0.05, 1.03, 1.6], 30, 0.22, -3) },
  { id: "street", a: W(9) - 4, light: "day", cam: glide([-18, 8, 9.5], [-10, 3.4, 7.2], [6, 2.6, -1], [0, 1.8, 0.8], 46) },
  { id: "walk", a: W(16) - 3, light: "day", cam: (f, u) => {
    const x = lerp(-13, -1.6, smooth(u));
    return { pos: [x + 2.4, 1.7, 6.4], look: [x + 0.4, 1.2, 2.2], fov: 38 };
  } },
  { id: "plain", a: W(25) - 3, light: "day", cam: push([0.35, 1.5, 3.7], [-0.45, 1.15, 1.7], 36, 0.16, 4) },
  { id: "name", a: W(28) - 3, light: "day", cam: push([0.1, 1.28, 2.45], [-0.05, 1.07, 1.6], 28, 0.2) },
  { id: "box", a: W(39) - 3, light: "day", cam: push([1.05, 1.6, 2.95], [0.25, 1.0, 1.6], 32, 0.18, -4) },
  { id: "manual", a: W(46) - 3, light: "day", cam: push([0.5, 1.9, 2.6], [0.4, 0.98, 1.6], 32, 0.15) },
  { id: "price", a: W(52) - 3, light: "day", cam: push([1.5, 1.45, 3.5], [0.35, 1.05, 1.65], 32, 0.2, 3) },
  { id: "crowd", a: W(56) - 3, light: "day", cam: push([0.3, 1.55, 8.2], [0.2, 1.2, 3.0], 40, 0.1) },
  { id: "million", a: W(61) - 3, light: "day", cam: glide([4, 9, 16], [10, 26, 26], [0, 0, 5], [0, 0, 4], 46) },
  { id: "rich", a: W(71) - 3, light: "golden", cam: push([0.7, 1.6, 6.2], [-0.55, 1.2, 1.9], 34, 0.16, -4) },
  { id: "moral", a: W(74) - 3, light: "golden", cam: push([0.15, 1.25, 2.6], [-0.05, 1.05, 1.6], 30, 0.22) },
  { id: "question", a: W(84) - 3, light: "golden", cam: push([-0.3, 1.55, 5.4], [-0.75, 1.2, 1.75], 34, 0.16) },
];

export const shotAt = (f: number) => {
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (f >= SHOTS[k].a) i = k;
  const s = SHOTS[i], end = i + 1 < SHOTS.length ? SHOTS[i + 1].a : TOTAL;
  return { shot: s, index: i, u: span(f, s.a, end), local: f - s.a };
};

/** a white flash after the hook */
export const FLASH_AT = SHOTS[1].a;

// story beats (frames)
export const BEAT = {
  coins: W(5), drop: W(45), manual: W(48), price: W(54), laugh: W(57), buy: W(59),
  stacks0: W(61), stacks1: W(70) + 10, rich: W(72), hikoya: W(79), end: W(88),
};
