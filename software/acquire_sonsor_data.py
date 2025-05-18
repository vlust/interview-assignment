#!/usr/bin/env python3
import argparse
import time
import random
import threading
import serial
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description="Read serial data for a specified duration and plot it")
    p.add_argument(
        "--port",
        default="loop://",
        help="Serial port URL (e.g. loop:// or COM3 or /dev/pts/5)",
    )
    p.add_argument("--baud", type=int, default=9600)
    p.add_argument("--outfile", default="output.png", help="Where to save the plot")
    p.add_argument("--test",    action="store_true", help="Run built-in emulator (loop:// only)")
    p.add_argument("--duration", type=float, default=60.0, help="Duration in seconds to record data")
    args = p.parse_args()

    ser = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1)
    # start emulator if requested (only works on loop://)
    if args.test and args.port.startswith("loop://"):
        # only import emulator when needed
        from emulator import start_emulator
        start_emulator(ser, args.duration)
    print(f"[plot_data] Listening on {args.port} for {args.duration} seconds...")

    start = time.time()
    timestamps = []
    values = []

    while True:
        line = ser.readline()  # expects newline‐terminated text, e.g. "12.34\n"
        now = time.time() - start

        if line:
            try:
                # convert to float; strip newline
                val = float(line.decode(errors="ignore").strip())
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
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor Value (e.g. mA→scaled)")
    plt.title(f"{int(args.duration)} s Snippet")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.outfile)
    print(f"[plot_data] Saved plot to {args.outfile}")
    # Optionally: plt.show()

if __name__ == "__main__":
    main()
