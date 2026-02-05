# Job Log: Update usage guide with terminal + GPU usage fields

**Job Date/Time**: 2026-02-05T075514

## Job Overview
Update the documentation `06_docs/11_16_scalability_test_gpu_usage.md` to match the current behavior of `03_script/16_scalability_test_gpu.py`, including tee-style duration logging to the running terminal and new GPU usage fields.

## Work Content

### 1. Duration-mode output behavior
- Documented that duration mode now reports to:
  - Terminal (stdout) in realtime
  - Output file when `--output PATH` is provided
- Added a concise description of the duration-mode header diagnostics (backend, PID, versions, CUDA_VISIBLE_DEVICES, GPU device info).

### 2. New periodic log fields
- Documented newly reported GPU usage indicators:
  - `gpu_mem_mb=used/total` (best-effort via `nvidia-smi`)
  - `proc_gpu_mem_mb` (best-effort via `nvidia-smi --query-compute-apps`)
- Added an example log line showing the new fields.

### 3. Troubleshooting updates
- Added notes about:
  - Duty-cycle pacing (`--util-max`) lowering average GPU utilization by design
  - Short-burst kernel workloads and `nvidia-smi` sampling limitations
- Added a recommended measurement setting: `--util-max 0` to disable pacing.

## Changed Files
- Modified: `06_docs/11_16_scalability_test_gpu_usage.md`
- New: `02_log/02_job/20260205T075514_update_usage_guide_with_terminal_gpu_usage_fields.md` (this job log)

## Result
- The usage guide now reflects the current runtime logging and GPU usage reporting behavior of the scalability test script.

