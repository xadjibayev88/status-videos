// Pet Rock short: one toon world posed per frame from story.ts; post = ink -> neutral tone map -> colour grade.
import React, { useEffect, useMemo } from "react";
import * as THREE from "three";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame } from "remotion";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import { World } from "./world";
import { FLASH_AT } from "./story";

const Inner: React.FC = () => {
  const f = useCurrentFrame();
  const { camera, scene, gl } = useThree();
  const world = useMemo(() => new World(), []);
  useEffect(() => { gl.toneMapping = THREE.NeutralToneMapping; gl.toneMappingExposure = 1.0; }, [gl]);
  world.update(f, camera as THREE.PerspectiveCamera, scene);
  return <primitive object={world.root} dispose={null} />;
};

export const PetRock: React.FC = () => {
  const f = useCurrentFrame();
  const flash = f >= FLASH_AT && f < FLASH_AT + 4 ? [1, 0.75, 0.45, 0.2][f - FLASH_AT] : 0;
  return (
    <AbsoluteFill style={{ background: "#bcd3ee" }}>
      <ThreeCanvas style={{ filter: "saturate(1.08) contrast(1.03)" }} width={1080} height={1920} gl={{ antialias: false, stencil: false, preserveDrawingBuffer: true }} camera={{ fov: 36, near: 0.05, far: 600 }}>
        <Inner />
      </ThreeCanvas>
      {flash > 0 && <AbsoluteFill style={{ background: "#ffffff", opacity: flash }} />}
      <Audio src={staticFile("voice/petrock.mp3")} />
    </AbsoluteFill>
  );
};
