# Job Log: Initialize Project (venv + requirements)

**Job Date/Time**: 2026-02-05T143500

## Job Overview
Initialize the project locally: create Python virtual environment (venv) and install dependencies from `requirements.txt`.

## Work Content

### 1. Virtual Environment (venv)
- **Method**: `python3 -m venv venv --without-pip` (system had no `ensurepip`; `python3-venv` package not installed)
- **Pip bootstrap**: Downloaded `get-pip.py` and ran with `./venv/bin/python get-pip.py`; pip 26.0.1 installed successfully
- **Result**: `venv/` created at project root; activate with `source venv/bin/activate` (Linux/Mac)

### 2. Requirements Installation
- **Full install**: `pip install -r requirements.txt` failed because `xhtml2pdf` depends on `pycairo`, which requires the system library **cairo** (not found: `Dependency "cairo" not found, tried pkgconfig`).
- **Core packages installed** (without `xhtml2pdf`):
  - numpy, matplotlib, scipy, markdown, PyMuPDF, pytesseract, Pillow, mpmath (and their dependencies)
- **Not installed**: `xhtml2pdf>=0.2.0` (blocked by missing system cairo)

### 3. Optional: Full requirements (including xhtml2pdf)
To install **xhtml2pdf** and complete `requirements.txt`:
1. Install system dependency: `sudo apt install libcairo2-dev` (Debian/Ubuntu)
2. Then run: `source venv/bin/activate && pip install -r requirements.txt`

### 4. Optional: Standard venv creation
If you prefer venv with ensurepip (no get-pip workaround):
- Install: `sudo apt install python3.12-venv`
- Recreate: `rm -rf venv && python3 -m venv venv` then `pip install -r requirements.txt` (after installing cairo if needed)

## Changed Files
- New: `venv/` (virtual environment directory)
- New: `02_log/02_job/20260205T143500_init_venv_requirements.md` (this job log)

## Result
- venv created and usable; core dependencies installed
- Scripts that do not use xhtml2pdf (e.g. visualization, PyMuPDF-based conversion) can run with current venv
- For markdown-to-PDF via xhtml2pdf, install `libcairo2-dev` and re-run `pip install -r requirements.txt`
