# WisprFlow

A lightweight Windows speech-to-text tool that transcribes your voice and pastes the result wherever your cursor is. Hold **Ctrl+Alt** to record, release to transcribe and paste instantly.

Powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — runs fully offline, no API key needed.

## Features

- Hold **Ctrl+Alt** → speak → release → text is pasted at cursor
- System tray icon shows current state (loading / idle / recording / transcribing)
- Works on any keyboard layout (AZERTY, QWERTY, etc.)
- Configurable Whisper model size, language, VAD filter, and custom corrections
- Optional auto-start at Windows login

## Requirements

- Windows 10/11
- Python 3.10+

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/wisprflow.git
cd wisprflow

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your config file
copy config.example.json config.json
```

Then edit `config.json` to your liking (see [Configuration](#configuration) below).

## Usage

```bash
# Run with a visible console (for debugging)
python main.py

# Run silently in the background (no console window)
pythonw wisprflow.pyw
# or double-click launch_wisprflow.bat
```

To add WisprFlow to Windows startup, run `install_startup.bat` once (no admin rights needed).

## Configuration

Copy `config.example.json` to `config.json` and edit it:

| Key | Default | Description |
|-----|---------|-------------|
| `model_size` | `"base"` | Whisper model: `tiny`, `base`, `small`, `medium`, `large-v3` |
| `language` | `null` | Force a language code (`"en"`, `"fr"`, …) or `null` for auto-detect |
| `device` | `"cpu"` | `"cpu"` or `"cuda"` (requires CUDA-compatible GPU) |
| `compute_type` | `"int8"` | `"int8"`, `"float16"`, `"float32"` |
| `beam_size` | `5` | Decoding beam size (higher = more accurate but slower) |
| `vad_filter` | `true` | Filter out silence with Voice Activity Detection |
| `initial_prompt` | `""` | Hint to help the model recognize domain-specific words |
| `corrections` | `{}` | Map of `"wrong phrase": "Correct Phrase"` applied after transcription |

**Example `config.json` with corrections:**

```json
{
    "model_size": "base",
    "language": null,
    "device": "cpu",
    "compute_type": "int8",
    "initial_prompt": "GitHub, API, JSON, Python",
    "corrections": {
        "git hub": "GitHub",
        "j s o n": "JSON"
    }
}
```

## Model sizes

| Model | VRAM | Speed | Accuracy |
|-------|------|-------|----------|
| tiny  | ~1 GB | fastest | lowest |
| base  | ~1 GB | fast | good |
| small | ~2 GB | moderate | better |
| medium | ~5 GB | slow | great |
| large-v3 | ~10 GB | slowest | best |

The model is downloaded automatically on first run (~150 MB for `base`).

## License

MIT
