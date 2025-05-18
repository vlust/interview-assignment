#!/usr/bin/env python3
import argparse
import datetime
import subprocess
import os
from typing import Any, Dict


def get_git_remote() -> str:
    """Return git remote URL or empty string if not available."""
    try:
        return subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except subprocess.CalledProcessError:
        return ""


def get_git_commit() -> str:
    """Return current git commit hash or empty string if not available."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except subprocess.CalledProcessError:
        return ""


def generate_report(
    cli_args: Dict[str, Any],
    data: Dict[str, Any],
    script_file: str,
    plot_path: str,
    out_tex: str = 'report.tex',
) -> None:
    """
    Generate a LaTeX report from sensor data and compile to PDF.

    Args:
        cli_args: Command-line arguments dictionary.
        data: Sensor data with keys 'timestamps' and 'values'.
        script_file: Path to the data acquisition script.
        plot_path: Path to the generated plot image.
        out_tex: Output .tex filename for the report.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # helper to escape LaTeX special chars
    def latex_escape(s: str) -> str:
        """Escape underscores for LaTeX."""
        return s.replace('_', '\\_')
    git_remote = get_git_remote()
    git_commit = get_git_commit()
    port = latex_escape(cli_args.get('port', ''))
    baud = cli_args.get('baud', '')
    test_mode = cli_args.get('test', False)
    duration = cli_args.get('duration', '')
    script_name = latex_escape(os.path.basename(script_file))
    plot_name = os.path.basename(plot_path)

    # Load LaTeX template and substitute placeholders
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'report_template.tex'))
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    subs = {
        'script': script_name,
        'port': port,
        'baud': baud,
        'test_mode': test_mode,
        'duration': duration,
        'git_remote': latex_escape(git_remote),
        'git_commit': latex_escape(git_commit),
        'timestamp': timestamp,
        'plot_name': plot_name,
    }
    for key, val in subs.items():
        template = template.replace(f'{{{key}}}', str(val))

    with open(out_tex, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Report written to {out_tex}")

    
    tex_dir, tex_file = os.path.split(out_tex)
    cmd = ['pdflatex', '-interaction=nonstopmode', tex_file]
    subprocess.run(cmd, cwd=tex_dir or '.', check=True)
    pdf_file = os.path.splitext(out_tex)[0] + '.pdf'
    print(f"PDF generated at {pdf_file}")
