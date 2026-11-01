# Desktop and self-hosted apps (owner's computer)

These are full applications, not Claude skills, so they install on the owner's Windows PC (LOT4019, no GPU) or a server, not in the cloud office. Office rule: never spend money, so anything that needs a paid key stays off.

| App | Repo | License | Runs on | Cost | Office verdict |
|---|---|---|---|---|---|
| VoiceStudio | [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | AGPL-3.0 | Windows installer or Docker, local | free, offline | **Try first.** Local voice cloning from a short clip, TTS, dubbing. Could give a free clone of the owner's voice. Slow on CPU; check Uzbek quality before using it for videos. |
| OpenWhispr | [OpenWhispr/openwhispr](https://github.com/OpenWhispr/openwhispr) | MIT | Windows app | free with local Whisper | **Useful.** Hotkey dictation: speak Uzbek, text appears at the cursor. Good for giving the office long instructions and for writing scripts by voice. Use the local engine (cloud mode may cost). |
| AppFlowy | [AppFlowy-IO/AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | AGPL-3.0 | Windows app | free locally | Optional. Notion-style notes and boards for content plans. The office already keeps plans in GitHub (`work/`), so only if the owner wants a visual board. |
| OpenProject | [opf/openproject](https://github.com/opf/openproject) | GPL-3.0 | server (Docker, PostgreSQL) | free self-hosted, needs an always-on server | Not now. Built for teams; a one-person office does not need a project server, and the PC is not always on. |
| OpenSEO | [every-app/open-seo](https://github.com/every-app/open-seo) | MIT | Docker or Cloudflare Workers | needs a **paid DataForSEO** key | Not used: it cannot work without paying DataForSEO. Keyword work stays with `seo-specialist` and vidIQ/YouTube data. |

## Install on Windows (owner)
1. **VoiceStudio**: open https://github.com/debpalash/VoiceStudio/releases, download the Windows installer (`.exe`/`.msi`) from the latest release, install, open it. Voice Clone -> record 10-30 s of clear Uzbek speech -> type an Uzbek line -> generate. If the result sounds right, save the clip to `inbox/` and tell the office.
2. **OpenWhispr**: open https://github.com/OpenWhispr/openwhispr/releases, download the Windows installer, install. Settings -> transcription -> Local (Whisper) -> language Uzbek. Press the hotkey, speak, release.
3. **AppFlowy** (optional): https://github.com/AppFlowy-IO/AppFlowy/releases -> Windows installer -> use it offline without an account.
