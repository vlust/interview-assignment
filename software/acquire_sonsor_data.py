#!/usr/bin/env python3
import argparse
import time
import serial
import os
import datetime
from argparse import Namespace
from pathlib import Path

from lib.data_acquirer import acquire_data
from lib.plotter import plot_data
from lib.report import generate_report


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

    outdir = Path(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    ser = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1)
    # start emulator if requested (only works on loop://)
    if args.test and args.port.startswith("loop://"):
        from lib.emulator import start_emulator
        start_emulator(ser, args.duration)
    print(f"[cli] Listening on {args.port} for {args.duration} seconds...")

    # Acquire data
    timestamps, values = acquire_data(ser, args.duration, outdir)
    ser.close()
    print("[cli] Done acquiring. Generating plot...")

    # Plot data
    plot_path = plot_data(timestamps, values, args.duration, outdir, date_str)

    # Generate LaTeX report
    report_filename = f"report_{date_str}.tex"
    report_path = os.path.join(outdir, report_filename)
    generate_report(vars(args), {'timestamps': timestamps, 'values': values}, __file__, plot_path, report_path)


if __name__ == "__main__":
    main()