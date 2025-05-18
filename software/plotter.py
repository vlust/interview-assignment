#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
from typing import List
from pathlib import Path

def plot_data(timestamps: List[float], values: List[float], duration: float, outdir: Path, date_str: str) -> str:
    """
    Generate and save plot from timestamps and values, return the file path.
    """
    plt.figure(figsize=(8,4))
    plt.plot(timestamps, values, marker="o", linestyle="-")
    plt.xlabel("Time [s]")
    plt.ylabel("Sensor Value [mA]")
    plt.title(f"{int(duration)} s Snippet")
    plt.grid(True)
    plt.tight_layout()
    plot_filename = f"plot_{date_str}.png"
    plot_path = os.path.join(outdir, plot_filename)
    plt.savefig(plot_path)
    print(f"[plot_data] Saved plot to {plot_path}")
    return plot_path
