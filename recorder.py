import threading
import numpy as np
import sounddevice as sd


class AudioRecorder:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self._chunks: list = []
        self._lock = threading.Lock()
        self._stream = None

    def _callback(self, indata: np.ndarray, frames: int, time, status):
        if status:
            print(f"[recorder] {status}")
        with self._lock:
            self._chunks.append(indata[:, 0].copy())  # mono, channel 0

    def start(self):
        self._chunks = []
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        with self._lock:
            if not self._chunks:
                return np.zeros(0, dtype="float32")
            return np.concatenate(self._chunks)
