#!/usr/bin/env python3
import time
from typing import List, Any, Tuple
from pathlib import Path
import csv
from datetime import datetime

def acquire_data(ser: Any, duration: float, out_dir: Path) -> Tuple[List[float], List[float]]:
    """
    Read from serial port for the specified duration and return timestamps and sensor values.
    """
    timestamps: List[float] = []
    values: List[float] = []
    start = time.time()
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csvfile = open(file_path, 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['timestamp', 'value'])

    while True:
        line = ser.readline()
        now = time.time() - start

        if line:
            try:
                val: float = float(line.decode(errors="ignore").strip())
                timestamps.append(now)
                values.append(val)
                writer.writerow([now, val])
                csvfile.flush()
                print(f"[{now:5.2f}s]  {val}")
            except ValueError:
                print(f"[{now:5.2f}s]  Invalid data: {line.decode(errors='ignore').strip()}")

        if now >= duration:
            break

    csvfile.close()
    return timestamps, values
