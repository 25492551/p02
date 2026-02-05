# Job Log: Update duration-mode terminal reporting + GPU usage checks

**Job Date/Time**: 2026-02-05T074743

## Job Overview
Improve `03_script/16_scalability_test_gpu.py` duration-mode observability by printing key runtime info to the running terminal (even when writing to an output file) and adding lightweight GPU usage checks (nvidia-smi utilization/memory + process GPU memory).

## Work Content

### 1. Make duration mode report to terminal while also writing to file
- Replaced the previous `sys.stdout` redirection approach with a small tee-style logger.
- Result: `--duration --output ...` now prints periodic summaries to the terminal and writes the same lines to the output file.

### 2. Add key runtime information to the header
- Added a startup header that reports:
  - Backend: CuPy (GPU) vs NumPy (CPU fallback)
  - PID
  - Python / NumPy / CuPy versions
  - CUDA_VISIBLE_DEVICES (if set)
  - GPU index, name, compute capability, and total memory (when available via CuPy)

### 3. Add GPU usage checks to periodic log lines
- Added lightweight nvidia-smi queries:
  - Per-GPU memory used/total and utilization (best-effort; may return n/a if nvidia-smi is unavailable)
  - Per-process GPU memory usage (MB) for the current PID (best-effort)
- Added new fields to each periodic log line:
  - `gpu_mem_mb=<used>/<total>`
  - `proc_gpu_mem_mb=<mb>`

### 4. Fix Python datetime deprecation warnings
- Replaced `datetime.utcnow()` with `datetime.now(timezone.utc)` in duration-mode logging.

### 5. Smoke test (venv)
- Ran short duration tests (`--duration` 6–15 seconds) to confirm:
  - Terminal output appears while writing to output file
  - Backend reports as CuPy (GPU) in this environment
  - GPU usage fields populate (GPU memory and process GPU memory)

## Changed Files
- Modified: `03_script/16_scalability_test_gpu.py`
- New: `02_log/02_job/20260205T074743_update_duration_terminal_reporting_gpu_usage_check.md` (this job log)

## Result
- Duration-mode runs now provide actionable runtime diagnostics in the terminal and in the output file, including confirmation of GPU backend selection and basic GPU usage indicators.

