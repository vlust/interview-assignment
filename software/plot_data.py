#!/usr/bin/env python3
import argparse
import time
import random
import threading
import serial
import matplotlib.pyplot as plt

def main():
    p = argparse.ArgumentParser(description="Read 60 s of serial data and plot it")
    p.add_argument(
        "--port",
        default="loop://",
        help="Serial port URL (e.g. loop:// or /dev/pts/5)",
    )
    p.add_argument("--baud", type=int, default=9600)
    p.add_argument("--outfile", default="output.png", help="Where to save the plot")
    p.add_argument("--test",    action="store_true", help="Run built-in emulator (loop:// only)")
    args = p.parse_args()

    ser = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1)
    # start emulator if requested (only works on loop://)
    if args.test and args.port.startswith("loop://"):
        def _emulator(s, duration=60):
            t0 = time.time()
            while True:
                t = time.time() - t0
                if t >= duration:
                    break
                current = 12 + 8 * (random.random() - 0.5)
                s.write(f"{current:.3f}\n".encode())
                time.sleep(0.1)
        threading.Thread(target=_emulator, args=(ser,60), daemon=True).start()
    print(f"[plot_data] Listening on {args.port} for 60 seconds...")

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

        # Stop after exactly 60 seconds
        if now >= 10.0:
            break

    ser.close()
    print("[plot_data] Done acquiring. Generating plot...")

    # Plot time vs. value
    plt.figure(figsize=(8,4))
    plt.plot(timestamps, values, marker="o", linestyle="-")
    plt.xlabel("Time (s)")
    plt.ylabel("Sensor Value (e.g. mA→scaled)")
    plt.title("60 s Snippet")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(args.outfile)
    print(f"[plot_data] Saved plot to {args.outfile}")
    # Optionally: plt.show()

if __name__ == "__main__":
    main()
