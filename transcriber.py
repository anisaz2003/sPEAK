import numpy as np
from faster_whisper import WhisperModel


class Transcriber:
    def __init__(self, model_size: str, device: str, compute_type: str,
                 language, beam_size: int, vad_filter: bool,
                 initial_prompt: str = "", corrections: dict = None):
        print(f"[transcriber] Loading model '{model_size}' on {device} ({compute_type})...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.language = language
        self.beam_size = beam_size
        self.vad_filter = vad_filter
        self.initial_prompt = initial_prompt or None
        self.corrections = {k.lower(): v for k, v in (corrections or {}).items()}
        print("[transcriber] Model ready.")

    def _apply_corrections(self, text: str) -> str:
        lower = text.lower()
        for wrong, right in self.corrections.items():
            lower_pos = lower.find(wrong)
            while lower_pos != -1:
                text = text[:lower_pos] + right + text[lower_pos + len(wrong):]
                lower = text.lower()
                lower_pos = lower.find(wrong, lower_pos + len(right))
        return text

    def transcribe(self, audio: np.ndarray) -> str:
        if audio.size < self.model.feature_extractor.hop_length * 10:
            return ""

        segments, info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=self.beam_size,
            vad_filter=self.vad_filter,
            vad_parameters={"min_silence_duration_ms": 300},
            initial_prompt=self.initial_prompt,
        )
        text = " ".join(seg.text.strip() for seg in segments).strip()
        if self.language is None and text:
            print(f"[transcriber] Detected language: {info.language} ({info.language_probability:.0%})")
        if self.corrections and text:
            text = self._apply_corrections(text)
        return text
