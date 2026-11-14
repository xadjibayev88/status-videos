// The Pet Rock world: one colourful toon street (1975), a shop table with the rock, boxes, crowd and effects.
// World meshes are inked by InkPass (layer 0); cards live on layer NOINK.
import * as THREE from "three";
import { NOINK } from "../lib/ink";
import { addOutlines } from "./outline";
import { Card, GARY_O, CROWD_O, drawPerson, burstCard, starsCard, coinsCard, moneyBagCard, priceCard } from "./cards";
import { SHOTS, shotAt, BEAT, ROCK, BOX, GARY, TABLE, smooth, span, lerp, type Light } from "./story";

const ramp = (() => {
  const d = new Uint8Array([70, 70, 70, 255, 150, 150, 150, 255, 255, 255, 255, 255]);
  const t = new THREE.DataTexture(d, 3, 1, THREE.RGBAFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true;
  return t;
})();
const toon = (color: THREE.ColorRepresentation, map?: THREE.Texture) => new THREE.MeshToonMaterial({ color, gradientMap: ramp, map: map ?? null });

const canvasTex = (w: number, h: number, paint: (g: CanvasRenderingContext2D) => void) => {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  paint(c.getContext("2d")!);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return t;
};
const skyTex = (top: string, hor: string) => canvasTex(4, 256, (g) => {
  const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, top); gr.addColorStop(0.75, hor); gr.addColorStop(1, hor);
  g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
});
const boxTex = canvasTex(256, 256, (g) => {
  g.fillStyle = "#c9955a"; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#b07d45"; g.fillRect(0, 0, 256, 34);
  g.fillStyle = "#2a1c18";
  for (let i = 0; i < 4; i++) for (let j = 0; j < 2; j++) { g.beginPath(); g.arc(52 + i * 50, 120 + j * 60, 9, 0, Math.PI * 2); g.fill(); }
});
const manualTex = canvasTex(256, 360, (g) => {
  g.fillStyle = "#f3e7c4"; g.fillRect(0, 0, 256, 360);
  g.fillStyle = "#2f6db3"; g.fillRect(0, 0, 256, 70);
  g.fillStyle = "#8d8a86"; g.beginPath(); g.ellipse(128, 210, 70, 50, 0.2, 0, Math.PI * 2); g.fill();
  g.strokeStyle = "#241726"; g.lineWidth = 8; g.stroke();
  g.fillStyle = "#241726"; for (let i = 0; i < 3; i++) g.fillRect(40, 290 + i * 18, 176 - i * 30, 8);
});

const SKY: Record<Light, { top: string; hor: string; fog: string; sun: string; sunI: number; hemiS: string; hemiG: string; hemiI: number; az: number; el: number; card: string }> = {
  day: { top: "#4f8ad6", hor: "#bcd3ee", fog: "#bcd3ee", sun: "#fff1dc", sunI: 3.0, hemiS: "#cfe0ff", hemiG: "#b39f84", hemiI: 1.25, az: 60, el: 48, card: "#ffffff" },
  golden: { top: "#f2a768", hor: "#ffd08a", fog: "#f6c893", sun: "#ffb36b", sunI: 3.3, hemiS: "#8f86c9", hemiG: "#6b4f5e", hemiI: 1.15, az: 125, el: 16, card: "#ffe3c4" },
};

const HOUSES = ["#b8624a", "#efe1c4", "#d9a441", "#c8743f", "#e9d6b0", "#9a5a46", "#d8b46a", "#c9684e"];

export class World {
  root = new THREE.Group();
  sun = new THREE.DirectionalLight("#ffffff", 3);
  hemi = new THREE.HemisphereLight("#ffffff", "#888888", 1);
  sky: Record<Light, THREE.Texture> = { day: skyTex(SKY.day.top, SKY.day.hor), golden: skyTex(SKY.golden.top, SKY.golden.hor) };
  rock: THREE.Mesh; box: THREE.Group; manual: THREE.Mesh; stacks: THREE.InstancedMesh; stackN = 0;
  gary = new Card(1.95); crowd: Card[] = []; burst = burstCard(); stars = starsCard(); coins = coinsCard(); bag = moneyBagCard(); price = priceCard();
  light: Light | null = null;

  constructor() {
    const r = this.root;
    r.add(this.sun, this.sun.target, this.hemi);
    // ground: sidewalk / road / far sidewalk / grass
    const strip = (z0: number, z1: number, col: string, y = 0) => {
      const m = new THREE.Mesh(new THREE.BoxGeometry(140, 0.12, z1 - z0), toon(col));
      m.position.set(0, y - 0.06, (z0 + z1) / 2); r.add(m);
    };
    strip(-40, 0, "#9fbf6a"); strip(0, 3.2, "#d9cdb4", 0.04); strip(3.2, 10.5, "#7d7a80"); strip(10.5, 13.5, "#d9cdb4", 0.04); strip(13.5, 60, "#9fbf6a");
    for (let x = -40; x <= 40; x += 6) { const h = new THREE.Mesh(new THREE.IcosahedronGeometry(1.1, 1), toon("#6aa84f")); h.position.set(x, 0.8, 15.5 + (x % 12 === 0 ? 1.2 : 0)); r.add(h); }
    for (let x = -60; x < 60; x += 4) { const d = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.02, 0.18), toon("#f2efe6")); d.position.set(x, 0.01, 6.85); r.add(d); }
    // two rows of houses
    const roofGeo = (w: number, d: number, h: number) => {
      const s = new THREE.Shape([new THREE.Vector2(-w / 2 - 0.3, 0), new THREE.Vector2(w / 2 + 0.3, 0), new THREE.Vector2(0, h)]);
      const g = new THREE.ExtrudeGeometry(s, { depth: d + 0.6, bevelEnabled: false }); g.translate(0, 0, -(d + 0.6) / 2); return g;
    };
    const house = (x: number, zFront: number, dir: 1 | -1, i: number, shop = false) => {
      const w = 7.2, d = 6, h = [7, 8.4, 9.8][i % 3];
      const grp = new THREE.Group(); grp.position.set(x, 0, zFront - (dir * d) / 2); if (dir < 0) grp.rotation.y = Math.PI;
      const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), toon(shop ? "#efe6cf" : HOUSES[i % HOUSES.length])); body.position.y = h / 2; grp.add(body);
      const roof = new THREE.Mesh(roofGeo(w, d, 2.4), toon(i % 2 ? "#7a3b34" : "#5a4a5e")); roof.position.y = h; grp.add(roof);
      const plinth = new THREE.Mesh(new THREE.BoxGeometry(w + 0.1, 0.7, d + 0.1), toon("#9b8f86")); plinth.position.y = 0.35; grp.add(plinth);
      const win = toon("#6d93c4"), frame = toon("#f4efe2");
      for (const wx of [-2.3, 0, 2.3]) for (const wy of shop ? [h - 2.2] : [h - 2.2, h - 4.6]) {
        if (wy < 2.5) continue;
        const fr = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.8, 0.12), frame); fr.position.set(wx, wy, d / 2 + 0.03); grp.add(fr);
        const gl = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.5, 0.14), win); gl.position.set(wx, wy, d / 2 + 0.04); grp.add(gl);
      }
      const door = new THREE.Mesh(new THREE.BoxGeometry(1.3, 2.4, 0.16), toon(shop ? "#2f6b4a" : "#6b3e2a")); door.position.set(shop ? 2.4 : 0, 1.2, d / 2 + 0.05); grp.add(door);
      if (shop) {
        const vit = new THREE.Mesh(new THREE.BoxGeometry(3.6, 2.2, 0.14), win); vit.position.set(-1.2, 1.9, d / 2 + 0.05); grp.add(vit);
        const awn = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.16, 1.8), toon("#d8463a")); awn.position.set(0, 3.55, d / 2 + 0.85); awn.rotation.x = -0.32; grp.add(awn);
        for (let k = -3; k <= 3; k += 2) { const st = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.17, 1.82), toon("#f4efe2")); st.position.set(k * 0.94, 3.555, d / 2 + 0.85); st.rotation.x = -0.32; grp.add(st); }
      }
      r.add(grp);
    };
    let i = 0;
    for (let x = -32; x <= 32; x += 8) house(x, 0, 1, i++, x === 0);
    for (let x = -36; x <= 36; x += 8) house(x, 22, -1, i++ + 3);
    // trees and lamp posts along the far walk
    for (let x = -30; x <= 30; x += 10) {
      const t = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, 2.2, 8), toon("#6b4a32")); t.position.set(x + 4, 1.1, 12.2); r.add(t);
      const c = new THREE.Mesh(new THREE.IcosahedronGeometry(1.3, 1), toon("#5f9a45")); c.position.set(x + 4, 3.1, 12.2); r.add(c);
      const lp = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.09, 3.4, 8), toon("#2e3440")); lp.position.set(x - 1, 1.7, 0.55); r.add(lp);
      const lh = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 8), toon("#fff3c4")); lh.position.set(x - 1, 3.5, 0.55); r.add(lh);
    }
    // the table, cushion, rock, box, manual
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.08, 0.85), toon("#a5683c")); top.position.set(TABLE[0], TABLE[1] - 0.04, TABLE[2]); r.add(top);
    for (const [lx, lz] of [[-0.75, -0.35], [0.75, -0.35], [-0.75, 0.35], [0.75, 0.35]]) {
      const l = new THREE.Mesh(new THREE.BoxGeometry(0.07, TABLE[1] - 0.08, 0.07), toon("#7a4a2a")); l.position.set(TABLE[0] + lx, (TABLE[1] - 0.08) / 2, TABLE[2] + lz); r.add(l);
    }
    const cloth = new THREE.Mesh(new THREE.BoxGeometry(1.74, 0.02, 0.4), toon("#e8dcc0")); cloth.position.set(0, TABLE[1] + 0.01, TABLE[2] + 0.24); r.add(cloth);
    const cushion = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.07, 0.26), toon("#c0353a")); cushion.position.set(ROCK[0], TABLE[1] + 0.035, ROCK[2]); r.add(cushion);
    const rg = new THREE.IcosahedronGeometry(0.075, 3);
    const pos = rg.attributes.position as THREE.BufferAttribute;
    for (let k = 0; k < pos.count; k++) {
      const v = new THREE.Vector3().fromBufferAttribute(pos, k);
      const n = 1 + 0.12 * Math.sin(v.x * 40 + 1.3) * Math.cos(v.z * 33) + 0.08 * Math.sin(v.y * 51);
      v.multiplyScalar(n); v.y *= 0.72; pos.setXYZ(k, v.x, v.y, v.z);
    }
    rg.computeVertexNormals();
    this.rock = new THREE.Mesh(rg, toon("#9a948c")); r.add(this.rock);
    this.box = new THREE.Group();
    const bm = toon("#c9955a", boxTex);
    const bx = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.2, 0.24), bm); bx.position.y = 0.1; this.box.add(bx);
    this.box.position.set(BOX[0], BOX[1], BOX[2]); r.add(this.box);
    this.manual = new THREE.Mesh(new THREE.BoxGeometry(0.17, 0.012, 0.24), [toon("#f3e7c4"), toon("#f3e7c4"), toon("#ffffff", manualTex), toon("#f3e7c4"), toon("#f3e7c4"), toon("#f3e7c4")]);
    r.add(this.manual);
    // a sea of boxes for "one and a half million"
    const N = 1400;
    this.stacks = new THREE.InstancedMesh(new THREE.BoxGeometry(0.3, 0.2, 0.24), bm, N);
    const mtx = new THREE.Matrix4(), q = new THREE.Quaternion();
    let n = 0;
    for (let layer = 0; layer < 4 && n < N; layer++) for (let gz = 0; gz < 24 && n < N; gz++) for (let gx = 0; gx < 60 && n < N; gx++) {
      const x = (gx - 30) * 0.36 + ((gz * 7 + layer * 3) % 5) * 0.012, z = 2.3 + gz * 0.4;
      if (Math.abs(x) < 1.2 && z < 3.2) continue;
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), (((gx * 13 + gz * 7 + layer) % 9) - 4) * 0.04);
      mtx.compose(new THREE.Vector3(x, 0.1 + layer * 0.205, z), q, new THREE.Vector3(1, 1, 1));
      this.stacks.setMatrixAt(n++, mtx);
    }
    this.stackN = n; this.stacks.count = 0; r.add(this.stacks);
    // cards
    r.add(this.gary.mesh);
    const spots: [number, number, number][] = [[-2.3, 3.4, 1.9], [-1.4, 4.1, 1.85], [-0.5, 3.6, 1.95], [0.5, 4.2, 1.8], [1.4, 3.5, 1.9], [2.3, 4.0, 1.85], [0.05, 4.9, 1.95]];
    spots.forEach(([x, z, h], k) => { const c = new Card(h); c.mesh.position.set(x, 0, z); this.crowd.push(c); r.add(c.mesh); });
    for (const c of [this.burst, this.stars, this.coins, this.bag, this.price]) { c.mesh.visible = false; r.add(c.mesh); }
    addOutlines(r);
  }

  setLight(l: Light, scene: THREE.Scene, cam: THREE.Camera) {
    const s = SKY[l];
    if (this.light !== l) {
      scene.background = this.sky[l];
      scene.fog = new THREE.Fog(s.fog, 28, 220);
      this.sun.color.set(s.sun); this.sun.intensity = s.sunI;
      this.hemi.color.set(s.hemiS); this.hemi.groundColor.set(s.hemiG); this.hemi.intensity = s.hemiI;
      for (const c of [this.gary, ...this.crowd, this.bag]) c.tint(s.card);
      this.light = l;
    }
    // camera-relative sun, frozen per shot
    const fwd = new THREE.Vector3(); cam.getWorldDirection(fwd); fwd.y = 0; fwd.normalize();
    const az = THREE.MathUtils.degToRad(s.az), el = THREE.MathUtils.degToRad(s.el);
    const dir = fwd.clone().applyAxisAngle(new THREE.Vector3(0, 1, 0), -az).multiplyScalar(Math.cos(el)); dir.y = Math.sin(el);
    this.sun.position.copy(dir.multiplyScalar(-40)).add(new THREE.Vector3(0, 0, 2));
    this.sun.position.y = Math.abs(this.sun.position.y) + 5;
    this.sun.target.position.set(0, 0, 2);
  }

  update(f: number, cam: THREE.PerspectiveCamera, scene: THREE.Scene) {
    const { shot, u, index } = shotAt(f);
    const c = shot.cam(f, u);
    cam.position.set(...c.pos); cam.fov = c.fov; cam.up.set(0, 1, 0); cam.lookAt(...c.look);
    if (c.roll) cam.rotateZ(THREE.MathUtils.degToRad(c.roll * (1 - 0.6 * u)));
    cam.updateProjectionMatrix();
    cam.layers.enable(NOINK);
    this.setLight(shot.light, scene, cam);
    const id = shot.id, blink = (f % 71) < 4;

    // rock: on the cushion, drops into the box on "solindi", back on the cushion for the moral
    const drop = id === "box" ? smooth(span(f, BEAT.drop - 6, BEAT.drop + 8)) : id === "manual" || id === "price" ? 1 : 0;
    const rx = lerp(ROCK[0], BOX[0], drop), ry = lerp(ROCK[1], BOX[1] + 0.12, drop) + Math.sin(Math.PI * drop) * 0.12, rz = ROCK[2];
    this.rock.position.set(rx, ry, rz);
    this.rock.rotation.set(0.15, f * 0.01 + 0.4, 0.05);
    this.rock.visible = drop < 0.98;
    // manual slides onto the box
    const man = id === "manual" ? smooth(span(f, BEAT.manual - 8, BEAT.manual + 6)) : id === "price" ? 1 : 0;
    this.manual.position.set(BOX[0] - 0.02, BOX[1] + 0.21 + (1 - man) * 0.25, BOX[2] + 0.01 + (1 - man) * 0.35);
    this.manual.rotation.set(0, -0.12, 0);
    this.manual.visible = man > 0.01;
    // boxes multiplying
    const k = id === "million" ? smooth(span(f, BEAT.stacks0 + 6, BEAT.stacks1)) : index > SHOTS.findIndex((s) => s.id === "million") ? 0 : 0;
    this.stacks.count = Math.floor(this.stackN * k);
    const sh = this.stacks.userData.shell as THREE.InstancedMesh | undefined; if (sh) sh.count = this.stacks.count;

    // Gary
    const g = this.gary;
    let gx = GARY[0], gz = GARY[2], mode: "stand" | "stroll" = "stand", expr: Parameters<typeof drawPerson>[2]["expr"] = "neutral", facing: -1 | 0 | 1 = 0, phase = 0, wave = 0;
    g.mesh.visible = !["hook", "box", "manual", "million", "moral"].includes(id);
    if (id === "walk") { gx = lerp(-13, -1.0, smooth(u)); gz = 2.25; mode = u < 0.97 ? "stroll" : "stand"; facing = mode === "stroll" ? 1 : 0; phase = (f / 16) % 1; expr = "whistle"; }
    if (id === "name") expr = "grin";
    if (id === "price") expr = "grin";
    if (id === "crowd") expr = f > BEAT.buy ? "grin" : "neutral";
    if (id === "rich") expr = "laugh";
    if (id === "question") { expr = "grin"; wave = smooth(span(f, BEAT.end - 20, BEAT.end + 10)); }
    g.mesh.position.set(gx, 0, gz);
    drawPerson(g, GARY_O, { mode, expr, facing, phase, blink, wave, seed: 7 }, `${mode}|${expr}|${facing}|${phase.toFixed(2)}|${blink}|${wave.toFixed(2)}`);
    g.face(cam);

    // crowd: laughs on "kulishdi", carries boxes from "sotib olishdi"
    this.crowd.forEach((cc, j) => {
      cc.mesh.visible = id === "crowd";
      if (!cc.mesh.visible) return;
      const laugh = f >= BEAT.laugh, buy = f >= BEAT.buy + j * 2;
      const e = laugh && !buy ? "laugh" : buy ? "grin" : "neutral";
      const bl = ((f + j * 17) % 83) < 4;
      drawPerson(cc, CROWD_O[j % CROWD_O.length], { mode: "stand", expr: e, blink: bl, seed: 30 + j, box: buy, headTilt: laugh && !buy ? (j % 2 ? 6 : -6) : 0 }, `${e}|${buy}|${bl}`);
      cc.face(cam);
    });

    // effects
    const pop = (t: number) => (t < 0 ? 0 : t < 1 ? 1.25 * Math.sin((t * Math.PI) / 2) - 0.25 * t * t : 1);
    this.coins.mesh.visible = id === "hook" && f >= BEAT.coins;
    if (this.coins.mesh.visible) { const t = span(f, BEAT.coins, BEAT.coins + 8); this.coins.mesh.position.set(ROCK[0], ROCK[1] + 0.12 + 0.05 * t, ROCK[2] - 0.35); this.coins.mesh.scale.setScalar(0.25 * pop(t)); this.coins.face(cam); }
    this.stars.mesh.visible = id === "name" && f >= BEAT.coins;
    if (this.stars.mesh.visible) { const t = span(f, SHOTS[4].a + 12, SHOTS[4].a + 22); this.stars.mesh.position.set(ROCK[0], ROCK[1] + 0.14, ROCK[2] + 0.02); this.stars.mesh.scale.setScalar(0.3 * pop(t)); this.stars.face(cam); }
    this.price.mesh.visible = id === "price" && f >= BEAT.price - 3;
    if (this.price.mesh.visible) { const t = span(f, BEAT.price - 3, BEAT.price + 5); this.price.mesh.position.set(BOX[0] + 0.25, BOX[1] + 0.12, BOX[2] + 0.18); this.price.mesh.scale.setScalar(0.62 * pop(t)); this.price.face(cam); }
    this.bag.mesh.visible = id === "rich";
    this.burst.mesh.visible = id === "rich" && f >= BEAT.rich;
    if (id === "rich") {
      this.bag.mesh.position.set(GARY[0] + 0.55, TABLE[1], GARY[2] - 0.1); this.bag.face(cam);
      const t = span(f, BEAT.rich, BEAT.rich + 8);
      this.burst.mesh.position.set(GARY[0], 1.3, GARY[2] - 0.6); this.burst.mesh.scale.setScalar(1.3 * pop(t)); this.burst.face(cam);
    }
    return new THREE.Vector3(...c.look);
  }
}
