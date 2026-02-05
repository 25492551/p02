# 16_scalability_test_gpu.py — Usage Guide

**File**: `03_script/16_scalability_test_gpu.py`  
**Purpose**: Run a GPU-accelerated (CuPy) scalability test for the Riemann zeta zero prediction pipeline, with options for parallel batch execution, dynamic GPU-memory batch capping, utilization pacing, and lightweight realtime logging.

---

## 1. Prerequisites

### 1.1 GPU / Driver / CUDA
- A CUDA-capable NVIDIA GPU.
- NVIDIA driver installed and working (`nvidia-smi` should run).
- CUDA Toolkit is recommended (the script can run with CuPy wheels, but system CUDA is typical).

### 1.2 Python venv
Activate the project virtual environment before running:

```bash
cd /home/seungun/Project/p02-main
source venv/bin/activate
```

### 1.3 Python packages
CuPy (CUDA 12.x):

```bash
pip install cupy-cuda12x
```

If CuPy is not installed, the script will fall back to NumPy (CPU), but GPU acceleration and stream parallelism will not apply.

---

## 2. What the script does (high-level)

For a set of zero indices \(n\) (range: `start_n..end_n` with `step`), the script runs a three-step prediction pipeline:

1. **Macroscopic prediction**: batched Newton solve of the inverse Riemann–von Mangoldt formula.
2. **Microscopic correction**: batched correction using a theoretical previous-zero approximation (to keep full batch parallelism).
3. **Chaos refinement**: batched Newton refinement of a Riemann–Siegel Z-function approximation.

To improve GPU utilization:
- Chaos function and its derivative are evaluated with a **single custom CUDA kernel** (CuPy `RawKernel`), avoiding large temporary 2D tensors.
- Independent batches can be pipelined across multiple **CuPy streams**.

---

## 3. Quick start

### 3.1 Single run (prints full stats)

```bash
python 03_script/16_scalability_test_gpu.py \
  --start-n 1000 --end-n 100000 --step 100 \
  --batch-size 10000
```

### 3.2 Higher parallelism (multiple streams)

To benefit from multi-stream pipelining, make sure the job has **multiple batches**:

```bash
python 03_script/16_scalability_test_gpu.py \
  --start-n 1000 --end-n 2000000 --step 100 \
  --batch-size 5000 \
  --double-buffer --streams 4
```

### 3.3 Duration run (3 hours) with utilization cap and light realtime logging

This is the recommended mode for long runs (prevents huge log files):

```bash
python 03_script/16_scalability_test_gpu.py \
  --duration 10800 \
  --output 06_docs/gpu_scalability_3h_lightlog_util87.txt \
  --start-n 1000 --end-n 2000000 --step 100 \
  --batch-size 5000 \
  --double-buffer --streams 4 \
  --util-max 87 \
  --log-interval-sec 10
```

Monitor in realtime:

```bash
tail -f 06_docs/gpu_scalability_3h_lightlog_util87.txt
```

---

## 4. Command-line options (most important)

### 4.1 Workload selection
- **`--start-n`** (int): first zero index. Default: `1000`.
- **`--end-n`** (int): last zero index. Default: `10000`.
- **`--step`** (int): stride in indices. Default: `100`.
- **`--batch-size`** (int): how many indices per batch. Default: `500`.

### 4.2 GPU memory safety (dynamic batch cap)
- **Enabled by default** on CuPy runs.
- **`--reserve-ratio`** (float): fraction of free GPU memory reserved (default `0.2`).
- **`--no-dynamic-memory`**: disable dynamic capping (risk of OOM).

### 4.3 Parallel batch execution (streams)
- **`--double-buffer`**: enable stream pipeline mode (only meaningful with CuPy and multiple batches).
- **`--streams N`**: number of CuPy streams used for pipelining (default `2`).

Notes:
- If you only have one batch, multiple streams will not increase utilization.
- For best effect, choose `end_n` and `batch-size` so that you have **many batches**.

### 4.4 Duration mode + logging
- **`--duration`** (seconds): run until time elapses (e.g. `10800` for 3 hours).
- **`--output PATH`**: write output to PATH (recommended for duration runs).
- **`--log-interval-sec`**: emit one-line summary every N seconds (default `10`).

### 4.5 Utilization cap (pacing)
- **`--util-max`**: target maximum utilization via duty-cycle pacing (default `87`).
- **`--max-sleep-sec`**: limit sleep per loop iteration (default `2`).
- **`--util-samples`**, **`--util-interval-sec`**: optional sampling of `nvidia-smi` utilization for reporting.

Important:
- This is implemented as a **duty-cycle cap** (sleep between runs). It does not hard-limit GPU utilization at the driver level.

---

## 5. Outputs

### 5.1 Single run
Prints a full per-run summary, including timing and error statistics.

### 5.2 Duration run (recommended for long runs)
Reports (tee-style logging):
- **Terminal (stdout)**: always prints a short header + periodic one-line summaries + final **`DURATION RUN SUMMARY`** block.
- **Output file** (when `--output PATH` is provided): writes the same header + periodic summaries + final summary to the file.

Header includes key runtime diagnostics:
- Backend selection: **CuPy (GPU)** vs **NumPy (CPU fallback)**
- PID
- Python / NumPy / CuPy versions
- `CUDA_VISIBLE_DEVICES` (if set)
- GPU device info (when available via CuPy): index, name, compute capability, total memory

Periodic one-line summaries include (in addition to throughput/error):
- `gpu_util%~=`: sampled GPU utilization average from `nvidia-smi` (best-effort)
- `gpu_mem_mb=used/total`: GPU memory used/total from `nvidia-smi` (best-effort)
- `proc_gpu_mem_mb=`: GPU memory used by the current PID from `nvidia-smi --query-compute-apps` (best-effort)

Example (single log line):
```text
2026-02-05T074736Z backend=cupy runs=5 (+5) zeros=9505 (+9505) ms/zero=0.011 err_mean%=0.1147 err_max%=0.7267 gpu_util%~=2.3 gpu_mem_mb=2780/24467 proc_gpu_mem_mb=226 sleep_added=0.00s rem=2s
```

---

## 6. Troubleshooting

### 6.1 GPU utilization is low
Common reasons:
- Too small workload (only one small batch).
- Too frequent CPU copies / logging (duration mode fixes this).
- Duty-cycle pacing enabled (`--util-max`) inserts sleep between runs, lowering average utilization by design.
- `nvidia-smi` utilization sampling can miss short bursty kernels; increase `--util-samples` and `--util-interval-sec` for more stable averages.

Fix:
- Increase `end_n` and/or reduce `batch-size` so multiple batches are created.
- Use `--double-buffer --streams 4` (or more) for pipelining.
- Disable pacing for measurement: `--util-max 0`

### 6.2 GitHub push rejected due to large log files
GitHub rejects files > 100 MB. Long-run logs can grow quickly.

Recommendations:
- Use duration mode (light logging) rather than verbose full outputs.
- Keep raw logs out of Git, or store only summaries.

---

## 7. Recommended presets

### 7.1 “High throughput”
```bash
python 03_script/16_scalability_test_gpu.py \
  --start-n 1000 --end-n 2000000 --step 100 \
  --batch-size 5000 \
  --double-buffer --streams 4
```

### 7.2 “3 hours, util <= 87%, light logs”
```bash
python 03_script/16_scalability_test_gpu.py \
  --duration 10800 \
  --output 06_docs/gpu_scalability_3h_lightlog_util87.txt \
  --start-n 1000 --end-n 2000000 --step 100 \
  --batch-size 5000 \
  --double-buffer --streams 4 \
  --util-max 87 \
  --log-interval-sec 10
```

