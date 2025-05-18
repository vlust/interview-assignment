#!/usr/bin/env python3
import time
import random
import threading
from typing import Any

def start_emulator(serial_obj: Any, duration: float) -> None:
    """
    Launches a background thread that writes synthetic sensor data to the given serial object
    for the specified duration in seconds.
    """
    def _emulator(s: Any, duration: float) -> None:
        t0 = time.time()
        while True:
            t = time.time() - t0
            if t >= duration:
                break
            current = 12 + 8 * (random.random() - 0.5)
            s.write(f"{current:.3f}\n".encode())
            time.sleep(0.1)
    threading.Thread(target=_emulator, args=(serial_obj, duration), daemon=True).start()