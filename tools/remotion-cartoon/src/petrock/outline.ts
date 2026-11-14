// Constant-screen-width ink outlines without post-processing (inverted hull): every world mesh gets a back-face
// shell pushed along its smoothed normals by a view-distance-proportional amount. Works in software WebGL.
import * as THREE from "three";
import { mergeVertices } from "three/examples/jsm/utils/BufferGeometryUtils.js";

const INK = new THREE.Color("#0b0a0c");
const cache = new WeakMap<THREE.BufferGeometry, THREE.BufferGeometry>();
const shellGeo = (g: THREE.BufferGeometry) => {
  let s = cache.get(g);
  if (!s) {
    const c = new THREE.BufferGeometry();
    c.setAttribute("position", g.getAttribute("position"));
    if (g.index) c.setIndex(g.index);
    s = mergeVertices(c, 1e-4); s.computeVertexNormals(); cache.set(g, s);
  }
  return s;
};
export const inkMaterial = (width = 0.0016) => {
  const m = new THREE.MeshBasicMaterial({ color: INK, side: THREE.BackSide, fog: true });
  m.onBeforeCompile = (sh) => {
    sh.uniforms.uInk = { value: width };
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nuniform float uInk;")
      .replace("#include <project_vertex>", `
        vec4 mvPosition = vec4( transformed, 1.0 );
        #ifdef USE_INSTANCING
          mvPosition = instanceMatrix * mvPosition;
        #endif
        mvPosition = modelViewMatrix * mvPosition;
        #ifdef USE_INSTANCING
          vec3 inkN = normalize( normalMatrix * mat3( instanceMatrix ) * normal );
        #else
          vec3 inkN = normalize( normalMatrix * normal );
        #endif
        mvPosition.xyz += inkN * uInk * max( 0.6, -mvPosition.z );
        gl_Position = projectionMatrix * mvPosition;`);
  };
  m.customProgramCacheKey = () => "ink-hull";
  return m;
};
const INK_MAT = inkMaterial();
/** add ink shells to every layer-0 mesh under root (call once, after building) */
export function addOutlines(root: THREE.Object3D) {
  const meshes: THREE.Mesh[] = [];
  root.traverse((o) => { const m = o as THREE.Mesh; if (m.isMesh && m.layers.mask === 1 && !m.userData.noInk) meshes.push(m); });
  for (const m of meshes) {
    const geo = shellGeo(m.geometry);
    let shell: THREE.Mesh;
    if ((m as THREE.InstancedMesh).isInstancedMesh) {
      const im = m as THREE.InstancedMesh, s = new THREE.InstancedMesh(geo, INK_MAT, im.instanceMatrix.count);
      s.instanceMatrix = im.instanceMatrix; s.count = im.count; shell = s;
      m.userData.shell = s;
    } else shell = new THREE.Mesh(geo, INK_MAT);
    shell.userData.noInk = true;
    shell.frustumCulled = m.frustumCulled;
    m.add(shell);
  }
}
