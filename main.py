import os
import threading
import time
from enum import Enum, auto

import keyboard
import sounddevice  # noqa: imported to surface PortAudio errors early

from config import load_config
from recorder import AudioRecorder
from transcriber import Transcriber
from paster import Paster
from tray import TrayIcon


class State(Enum):
    IDLE = auto()
    RECORDING = auto()
    TRANSCRIBING = auto()


class WisprFlow:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.state = State.IDLE
        self._lock = threading.Lock()
        self._tray: TrayIcon | None = None

        self.recorder = AudioRecorder(cfg["sample_rate"])
        self.transcriber = Transcriber(
            cfg["model_size"],
            cfg["device"],
            cfg["compute_type"],
            cfg["language"],
            cfg["beam_size"],
            cfg["vad_filter"],
            initial_prompt=cfg.get("initial_prompt", ""),
            corrections=cfg.get("corrections", {}),
        )
        self.paster = Paster()

    def set_tray(self, tray: TrayIcon):
        self._tray = tray

    def _set_state(self, new_state: State):
        self.state = new_state
        if self._tray:
            self._tray.set_state(new_state.name.lower())

    # ------------------------------------------------------------------ #
    # Hotkey handlers                                                      #
    # ------------------------------------------------------------------ #

    def on_hotkey_down(self):
        with self._lock:
            if self.state != State.IDLE:
                return
            self._set_state(State.RECORDING)

        try:
            self.recorder.start()
        except Exception as e:
            print(f"[main] Failed to start recording: {e}")
            with self._lock:
                self._set_state(State.IDLE)
            return

        print("[main] Recording...")

    def on_hotkey_up(self):
        with self._lock:
            if self.state != State.RECORDING:
                return
            self._set_state(State.TRANSCRIBING)

        threading.Thread(target=self._stop_and_paste, daemon=True).start()

    # ------------------------------------------------------------------ #
    # Transcription + paste                                                #
    # ------------------------------------------------------------------ #

    def _stop_and_paste(self):
        audio = self.recorder.stop()
        print("[main] Transcribing...")

        try:
            text = self.transcriber.transcribe(audio)
        except Exception as e:
            print(f"[main] Transcription error: {e}")
            with self._lock:
                self._set_state(State.IDLE)
            return

        if text:
            word_count = len(text.split())
            time.sleep(0.1)
            self.paster.paste(text)
            preview = text[:60] + ("..." if len(text) > 60 else "")
            print(f"[main] Pasted ({word_count} words): {preview}")
        else:
            print("[main] No speech detected.")

        with self._lock:
            self._set_state(State.IDLE)


# ---------------------------------------------------------------------- #
# Hotkey wiring                                                           #
# ---------------------------------------------------------------------- #

# Scan codes are language-independent (work on French/AZERTY keyboards)
# Left Ctrl=29, Right Ctrl=97, Left Alt=56, Right Alt=100
_CTRL_SCANCODES = {29, 97}
_ALT_SCANCODES  = {56, 100}


def setup_hotkey(app: WisprFlow):
    ctrl_held = False
    alt_held  = False

    def on_event(e):
        nonlocal ctrl_held, alt_held

        sc = e.scan_code
        is_down = e.event_type == keyboard.KEY_DOWN

        if sc in _CTRL_SCANCODES:
            ctrl_held = is_down
        elif sc in _ALT_SCANCODES:
            alt_held = is_down

        combo_active = ctrl_held and alt_held

        if is_down and combo_active:
            app.on_hotkey_down()
        elif not is_down and sc in (_CTRL_SCANCODES | _ALT_SCANCODES):
            app.on_hotkey_up()

    keyboard.hook(on_event, suppress=False)


# ---------------------------------------------------------------------- #
# App thread + shutdown                                                   #
# ---------------------------------------------------------------------- #

def _run_app(cfg: dict, tray: TrayIcon):
    """Runs in background thread: loads model then starts hotkey listener."""
    app = WisprFlow(cfg)       # model loads here (2-3s) — tray already visible
    app.set_tray(tray)
    tray.set_state("idle")     # blue → grey : modèle prêt
    setup_hotkey(app)
    keyboard.wait()


def _shutdown(tray: TrayIcon):
    keyboard.unhook_all()
    tray.stop()


def _restart(cfg: dict, tray: TrayIcon):
    """Unhook keyboard, reload model in a new background thread."""
    keyboard.unhook_all()
    tray.set_state("loading")
    app_thread = threading.Thread(target=_run_app, args=(cfg, tray), daemon=True)
    app_thread.start()


# ---------------------------------------------------------------------- #
# Entry point                                                             #
# ---------------------------------------------------------------------- #

def main():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    cfg = load_config(config_path)

    tray = TrayIcon(
        on_quit=lambda: _shutdown(tray),
        on_restart=lambda: _restart(cfg, tray),
    )

    # Load model in background — tray icon appears immediately (blue = loading)
    app_thread = threading.Thread(target=_run_app, args=(cfg, tray), daemon=True)
    app_thread.start()

    tray.run()  # blocks main thread — pystray Win32 message loop


if __name__ == "__main__":
    main()
