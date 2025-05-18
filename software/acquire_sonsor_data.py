#!/usr/bin/env python3
import argparse
import time
import random
import threading
import serial
import matplotlib.pyplot as plt
import os
import datetime
from report import generate_report
from argparse import Namespace
from typing import List, Any

def main() -> None:
    """
    Acquire serial sensor data for a given duration, plot the results, and generate a LaTeX report.
    """
    p = argparse.ArgumentParser(description="Read serial data for a specified duration and plot it")
    p.add_argument(
        "--port",
        default="loop://",
        help="Serial port URL (e.g. loop:// or COM3 or /dev/pts/5)",
    )
    p.add_argument("--baud", type=int, default=9600)
    p.add_argument(
        "--outdir",
        default=".",
        help="Directory to save outputs",
    )
    p.add_argument("--test",    action="store_true", help="Run built-in emulator (loop:// only)")
    p.add_argument("--duration", type=float, default=60.0, help="Duration in seconds to record data")
    args: Namespace = p.parse_args()

    # prepare output directory and filenames
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    ser: Any = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1)
    # start emulator if requested (only works on loop://)
    if args.test and args.port.startswith("loop://"):
        # only import emulator when needed
        from emulator import start_emulator
        start_emulator(ser, args.duration)
    print(f"[plot_data] Listening on {args.port} for {args.duration} seconds...")

    start = time.time()
    timestamps: List[float] = []
    values: List[float] = []

    while True:
        line = ser.readline()  # expects newline‐terminated text, e.g. "12.34\n"
        now = time.time() - start

        if line:
            try:
                # convert to float; strip newline
                val: float = float(line.decode(errors="ignore").strip())
                timestamps.append(now)
                values.append(val)
                print(f"[{now:5.2f}s]  {val}")
            except ValueError:
                # skip parse errors
                pass

        # Stop after exactly args.duration seconds
        if now >= args.duration:
            break

    ser.close()
    print("[plot_data] Done acquiring. Generating plot...")

    # Plot time vs. value
    plt.figure(figsize=(8,4))
    plt.plot(timestamps, values, marker="o", linestyle="-")
    plt.xlabel("Time [s]")
    plt.ylabel("Sensor Value [mA]")
    plt.title(f"{int(args.duration)} s Snippet")
    plt.grid(True)
    plt.tight_layout()
    # save plot with dated filename
    plot_filename = f"plot_{date_str}.png"
    plot_path = os.path.join(outdir, plot_filename)
    plt.savefig(plot_path)
    print(f"[plot_data] Saved plot to {plot_path}")
    # Generate LaTeX report including metadata, raw data and plot
    # generate report with dated filename
    report_filename = f"report_{date_str}.tex"
    report_path = os.path.join(outdir, report_filename)
    generate_report(vars(args), {'timestamps': timestamps, 'values': values}, __file__, plot_path, report_path)
    # Optionally: plt.show()

if __name__ == "__main__":
    main()
