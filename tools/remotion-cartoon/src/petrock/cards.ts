// Camera-facing 2D cards (characters, effects, small props) drawn with the skill's Canvas2D cartoon pen.
import * as THREE from "three";
import { Pen, bodyFront, townsfolk, INK, type Outfit, type FrontOpts, fxBurst, fxStars } from "../lib/toon";
import { NOINK } from "../lib/ink";

export const GARY_O: Outfit = { jacket: "#c8652a", pants: "#34466e", boots: "#3a2a22", hat: "hair", hair: "#4a2e1c", moustache: "#4a2e1c" };
export const CROWD_O: Outfit[] = [0, 1, 2, 3, 4, 5, 6].map((v) => townsfolk(v));

/** a flat card standing on its bottom edge; 600 x 1000 design units like toon.ts */
export class Card {
  canvas: HTMLCanvasElement; g: CanvasRenderingContext2D; tex: THREE.CanvasTexture; mesh: THREE.Mesh; mat: THREE.MeshBasicMaterial;
  key = "";
  constructor(public h: number, public aspect = 0.6, px = 640, public anchor: "bottom" | "center" = "bottom") {
    this.canvas = document.createElement("canvas");
    this.canvas.width = Math.round(px * aspect); this.canvas.height = px;
    this.g = this.canvas.getContext("2d")!;
    this.tex = new THREE.CanvasTexture(this.canvas);
    this.tex.colorSpace = THREE.SRGBColorSpace; this.tex.anisotropy = 4;
    this.mat = new THREE.MeshBasicMaterial({ map: this.tex, transparent: true, alphaTest: 0.04, fog: false });
    const geo = new THREE.PlaneGeometry(h * aspect, h);
    if (anchor === "bottom") geo.translate(0, h / 2 - h * 0.025, 0);
    this.mesh = new THREE.Mesh(geo, this.mat);
    this.mesh.layers.set(NOINK);
    this.mesh.renderOrder = 2;
  }
  draw(key: string, fn: (p: Pen, g: CanvasRenderingContext2D) => void) {
    if (key === this.key) return;
    this.key = key;
    const g = this.g;
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(0, 0, this.canvas.width, this.canvas.height);
    g.setTransform(this.canvas.width / (1000 * this.aspect), 0, 0, this.canvas.height / 1000, 0, 0);
    g.lineJoin = "round"; g.lineCap = "round";
    fn(new Pen(g), g);
    this.tex.needsUpdate = true;
  }
  /** yaw-only billboard (cards stay upright) */
  face(cam: THREE.Camera) {
    const p = this.mesh.getWorldPosition(new THREE.Vector3());
    this.mesh.rotation.set(0, Math.atan2(cam.position.x - p.x, cam.position.z - p.z), 0);
  }
  tint(c: THREE.ColorRepresentation) { this.mat.color.set(c); }
}

/** a little cardboard pet-rock box held in front of the torso */
export const heldBox = (g: CanvasRenderingContext2D, x = 300, y = 610) => {
  g.save();
  g.translate(x, y);
  g.fillStyle = "#c9955a"; g.strokeStyle = INK; g.lineWidth = 9;
  g.beginPath(); g.roundRect(-78, -52, 156, 104, 8); g.fill(); g.stroke();
  g.fillStyle = "#a9773f"; g.beginPath(); g.roundRect(-78, -52, 156, 26, 8); g.fill(); g.stroke();
  g.fillStyle = INK;
  for (const [hx, hy] of [[-40, 6], [0, 6], [40, 6], [-20, 30], [20, 30]]) { g.beginPath(); g.arc(hx, hy, 6, 0, Math.PI * 2); g.fill(); }
  g.restore();
};

export const drawPerson = (c: Card, o: Outfit, opts: FrontOpts & { box?: boolean }, key: string) =>
  c.draw(key, (p, g) => { bodyFront(p, o, opts); if (opts.box) heldBox(g); });

/** effect cards (centre-anchored, square) */
export const burstCard = () => {
  const c = new Card(1.6, 1, 512, "center");
  c.draw("burst", (p, g) => {
    g.translate(0, 0); // design space is 1000 x 1000 here
    g.save(); g.translate(500, 500); g.scale(1.9, 1.9); g.translate(-300, -500);
    fxBurst(p, 0.85, "#ffd34d", 12, 60, 240);
    g.restore();
  });
  return c;
};
export const starsCard = () => {
  const c = new Card(0.9, 1, 512, "center");
  c.draw("stars", (p, g) => { g.save(); g.translate(500, 560); g.scale(2.2, 2.2); g.translate(-300, -500); fxStars(p, 0.6); g.restore(); });
  return c;
};
export const coinsCard = () => {
  const c = new Card(1.4, 1, 512, "center");
  c.draw("coins", (_p, g) => {
    const coins: [number, number, number][] = [[230, 300, 70], [520, 220, 80], [760, 340, 64], [330, 620, 76], [650, 600, 70], [480, 430, 60]];
    for (const [x, y, r] of coins) {
      g.fillStyle = "#f2c230"; g.strokeStyle = INK; g.lineWidth = 12;
      g.beginPath(); g.ellipse(x, y, r, r * 0.92, 0, 0, Math.PI * 2); g.fill(); g.stroke();
      g.fillStyle = "#ffe48a"; g.beginPath(); g.ellipse(x - r * 0.25, y - r * 0.25, r * 0.28, r * 0.2, -0.6, 0, Math.PI * 2); g.fill();
      g.fillStyle = INK; g.font = `900 ${Math.round(r * 1.1)}px Arial Black, Arial, sans-serif`; g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText("$", x, y + 4);
    }
  });
  return c;
};
export const moneyBagCard = () => {
  const c = new Card(0.85, 1, 512, "bottom");
  c.draw("bag", (_p, g) => {
    g.fillStyle = "#c9a35c"; g.strokeStyle = INK; g.lineWidth = 16;
    g.beginPath();
    g.moveTo(400, 300); g.bezierCurveTo(150, 420, 120, 930, 500, 960); g.bezierCurveTo(880, 930, 850, 420, 600, 300); g.closePath();
    g.fill(); g.stroke();
    g.beginPath(); g.moveTo(400, 300); g.lineTo(330, 170); g.lineTo(670, 170); g.lineTo(600, 300); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = "#7a3b22"; g.fillRect(380, 280, 240, 34); g.strokeRect(380, 280, 240, 34);
    g.fillStyle = "#2f7a3a"; g.font = "900 300px Arial Black, Arial, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
    g.fillText("$", 500, 660);
  });
  return c;
};
export const priceCard = () => {
  const c = new Card(0.32, 1.6, 400, "center");
  c.draw("price", (_p, g) => {
    // design space 1600 x 1000
    g.fillStyle = "#fff6dc"; g.strokeStyle = INK; g.lineWidth = 34;
    g.beginPath(); g.moveTo(260, 120); g.lineTo(1480, 120); g.lineTo(1480, 880); g.lineTo(260, 880); g.lineTo(60, 500); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = INK; g.beginPath(); g.arc(250, 500, 50, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#d63a2f"; g.font = "900 560px Arial Black, Arial, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle";
    g.fillText("$4", 900, 530);
  });
  return c;
};
