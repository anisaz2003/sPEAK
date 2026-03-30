from PIL import Image, ImageDraw
import pystray


def _draw_mic(color: tuple) -> Image.Image:
    """Draw a 64x64 microphone icon in the given RGBA color."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    outline = (0, 0, 0, 180)

    # Mic body outline (slightly larger, dark)
    d.rounded_rectangle((18, 2, 46, 38), radius=12, fill=outline)
    # Mic body fill
    d.rounded_rectangle((21, 5, 43, 35), radius=10, fill=color)

    # Stand arc (U shape below body)
    d.arc((12, 26, 52, 54), start=0, end=180, fill=outline, width=5)
    d.arc((12, 26, 52, 54), start=0, end=180, fill=color, width=3)

    # Vertical post
    d.line([(32, 51), (32, 59)], fill=outline, width=5)
    d.line([(32, 51), (32, 59)], fill=color, width=3)

    # Base bar
    d.line([(20, 59), (44, 59)], fill=outline, width=5)
    d.line([(20, 59), (44, 59)], fill=color, width=3)

    return img


# Pre-render the state icons
_ICONS = {
    "loading":      _draw_mic((100, 100, 220, 255)),   # blue  — chargement
    "idle":         _draw_mic((160, 160, 160, 255)),   # grey  — prêt
    "recording":    _draw_mic((220,  50,  50, 255)),   # red   — enregistrement
    "transcribing": _draw_mic((230, 180,   0, 255)),   # amber — transcription
}

_TITLES = {
    "loading":      "WisprFlow — Loading model...",
    "idle":         "WisprFlow — Ready (Ctrl+Alt)",
    "recording":    "WisprFlow — Recording...",
    "transcribing": "WisprFlow — Transcribing...",
}


class TrayIcon:
    def __init__(self, on_quit, on_restart):
        menu = pystray.Menu(
            pystray.MenuItem("Restart", lambda icon, item: on_restart()),
            pystray.MenuItem("Quit",    lambda icon, item: on_quit()),
        )
        self._icon = pystray.Icon(
            name="WisprFlow",
            icon=_ICONS["loading"],
            title=_TITLES["loading"],
            menu=menu,
        )

    def set_state(self, state_name: str):
        """Update icon appearance. state_name: 'idle' | 'recording' | 'transcribing'"""
        self._icon.icon  = _ICONS[state_name]
        self._icon.title = _TITLES[state_name]

    def run(self):
        """Blocking — call from main thread."""
        self._icon.run()

    def stop(self):
        self._icon.stop()
