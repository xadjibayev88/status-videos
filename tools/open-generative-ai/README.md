# Open Generative AI (owner's computer only)

Source: [Anil-matcha/Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI), MIT, desktop app v2.0.0.

## What is free and what is not
- The app itself is free and open source.
- The 600+ cloud models (Kling, Veo, Sora, Midjourney, Flux, Seedream, lip sync...) run through MuAPI.ai and are **paid per generation**. Office rule: never spend money, so the office does not use a MuAPI key.
- Free path = **local models** on the owner's PC:
  - Images: sd.cpp engine (bundled). Dreamshaper 8 / Realistic Vision v5.1 (2.1 GB), SDXL (6.9 GB), Z-Image. Runs on CPU, faster on a GPU.
  - Video: Wan2GP (Wan 2.1 1.3B at 480p needs an NVIDIA/AMD GPU with ~8 GB VRAM; installed separately with Python).
- It cannot run inside GitHub Actions (no GPU), so the automations keep using stock footage.

## Install on Windows (LOT4019)
1. Download `Open Generative AI Setup 2.0.0.exe` from https://github.com/Anil-matcha/Open-Generative-AI/releases/tag/v2.0.0 and run it.
2. When it asks for a MuAPI key, skip it.
3. Settings -> Local Models -> install the sd.cpp engine -> download Realistic Vision v5.1.
4. Image Studio -> "Local" toggle -> pick the local model -> generate.
5. Optional, only with an NVIDIA GPU: install Wan2GP (https://github.com/deepbeepmeep/Wan2GP), then Settings -> Local Models -> Wan2GP -> set its folder -> Check.

## Office use
Covers, backgrounds and B-roll stills for Bilarmidingiz and apex_wealths; short 480p clips if the PC has a GPU. Put finished files in `inbox/` (videos) or `work/creative/<task>/` (images). Same brand and content rules as everything else: no real people's likeness, nothing misleading, no NSFW.
