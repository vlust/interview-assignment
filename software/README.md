# Current Sensor Reader

`current-sensor-reader` is a Python toolchain for acquiring serial data from a custom current sensor, plotting the measurements, and generating a LaTeX report.

## Features
- Read real-time current measurements over serial (supports physical COM ports and `loop://` emulator).
- Save raw data to a timestamped CSV file in an output directory.
- Plot measurements with Matplotlib.
- Generate a PDF report via LaTeX template (requires a LaTeX installation).

## Prerequisites
- Python >= 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation)
- A LaTeX distribution (e.g. TeX Live, MiKTeX) on your PATH to compile reports

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url> && cd interview-assignment/software
   ```

## Usage

Run the main CLI script to acquire data, generate a plot, and build a report:

```bash
uv run acquire_sonsor_data.py \
  --port COM3           # not needed for --test
  --baud 9600           # serial baud rate
  --duration 60         # acquisition duration (seconds)
  --outdir ./output     # directory to save CSV, plot, and report
  [--test]              # start built-in emulator (only valid with loop://)
```

### Example
```bash
uv run acquire_sonsor_data.py --port loop:// --test --duration 10 --outdir ./results
```
- Creates `results/data_YYYYMMDD_HHMMSS.csv` containing timestamp/value columns.
- Generates `results/plot_YYYYMMDD_HHMMSS.png` (or .pdf).
- Writes `results/report_YYYYMMDD_HHMMSS.tex` and compiles to PDF using the LaTeX template in the project root.


## License
[MIT](LICENSE)
