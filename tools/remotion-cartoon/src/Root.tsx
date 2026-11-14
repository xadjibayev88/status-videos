import React from "react";
import { Composition } from "remotion";
import { PetRock } from "./petrock/PetRock";
import { TOTAL } from "./petrock/story";

export const Root: React.FC = () => (
  <Composition id="PetRock" component={PetRock} durationInFrames={TOTAL} fps={30} width={1080} height={1920} />
);
