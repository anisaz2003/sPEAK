# sPEAK

Hold **Ctrl+Alt**, speak, release — your words are pasted instantly wherever your cursor is.

Powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper). Runs fully offline, no API key needed.

---

## Install

1. Install [Python 3.10+](https://www.python.org/downloads/) *(check "Add to PATH" during install)*
2. Clone or [download the repo](https://github.com/anisaz2003/sPEAK/archive/refs/heads/main.zip)
3. Double-click **`setup.bat`** — it installs everything automatically

## Run

- **Double-click `launch_wisprflow.bat`** — runs silently in the background
- A microphone icon appears in the system tray

> First launch downloads the Whisper model (~150 MB). This only happens once.

## Usage

| Action | Result |
|--------|--------|
| Hold **Ctrl+Alt** | Start recording |
| Release **Ctrl+Alt** | Transcribe and paste at cursor |
| Tray icon: grey | Ready |
| Tray icon: red | Recording |
| Tray icon: amber | Transcribing |

## Auto-start with Windows

Run **`install_startup.bat`** once — sPEAK will launch automatically at login.

## Configuration

Edit `config.json` (created by `setup.bat`):

| Key | Default | Description |
|-----|---------|-------------|
| `model_size` | `"base"` | `tiny` / `base` / `small` / `medium` / `large-v3` — bigger = more accurate but slower |
| `language` | `null` | Force a language (`"en"`, `"fr"`, …) or `null` for auto-detect |
| `device` | `"cpu"` | `"cpu"` or `"cuda"` for NVIDIA GPU |
| `initial_prompt` | `""` | Words to help recognition (e.g. `"GitHub, API, JSON"`) |
| `corrections` | `{}` | Post-transcription fixes: `{"git hub": "GitHub"}` |
