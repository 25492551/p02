#!/usr/bin/env python3
"""
GPU-optimized Scalability Test for Zero Prediction Algorithm.
Tests algorithm performance on zeros 1,000-10,000 using batched GPU computation.

Requires: pip install cupy-cuda12x  (for CUDA 12.x)
Falls back to NumPy (CPU) if CuPy is not available.

CLI: --duration SECONDS  Run until SECONDS elapsed (e.g. 10800 for 3 hours).
     --output PATH       Write all output to PATH (used with --duration).

For higher GPU utilization use larger workload and batch size, e.g.:
  --start-n 1000 --end-n 100000 --step 100 --batch-size 10000
See 06_docs/gpu_scalability_low_utilization_analysis.md for details.
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np

try:
    import cupy as cp
    _CUPY_AVAILABLE = True
except ImportError:
    _CUPY_AVAILABLE = False
    cp = None


def _get_array_module(use_gpu=True):
    """Return CuPy or NumPy depending on availability and flag."""
    if use_gpu and _CUPY_AVAILABLE:
        return cp
    return np


def get_gpu_safe_batch_size(n_cutoff=20, reserve_ratio=0.2, max_batch=10_000_000):
    """
    Compute a batch size that fits in current GPU free memory (CuPy only).
    Uses a conservative bytes-per-element estimate for predict_zero_three_step_batched.
    Returns (safe_batch_size, free_mb, total_mb) or (None, 0, 0) if not CuPy.
    """
    if not _CUPY_AVAILABLE:
        return None, 0, 0
    try:
        free_bytes, total_bytes = cp.cuda.runtime.memGetInfo()
        free_mb = free_bytes / (1024 ** 2)
        total_mb = total_bytes / (1024 ** 2)
        # Conservative: n_arr, t_macro, t_micro, t_final, theta, arg, term, intermediates (float64)
        # ~ (4 + 3 * n_cutoff) * 8 bytes per element
        bytes_per_element = 8 * (10 + 3 * n_cutoff)
        reserve = 1.0 - reserve_ratio
        safe = int((free_bytes * reserve) / bytes_per_element)
        safe = max(1, min(safe, max_batch))
        return safe, free_mb, total_mb
    except Exception:
        return None, 0, 0


_CHAOS_KERNEL_CACHE = {}


def _get_chaos_tables_cupy(n_cutoff, dtype):
    """Precompute log(n) and 1/sqrt(n) for chaos kernel (CuPy only)."""
    n_vec = cp.arange(1, n_cutoff + 1, dtype=dtype)
    log_n = cp.log(n_vec)
    inv_sqrt_n = 1.0 / cp.sqrt(n_vec)
    return log_n, inv_sqrt_n


def _get_chaos_kernel_and_tables(n_cutoff, dtype):
    """
    Return (raw_kernel, log_n, inv_sqrt_n) for given n_cutoff and dtype.
    Kernel computes both chaos wave value and derivative in one launch:
      out_f[i]  = 2 * sum cos(theta - t*log(n))/sqrt(n)
      out_fp[i] = 2 * sum -sin(arg)*(d_theta - log(n))/sqrt(n)
    """
    if not _CUPY_AVAILABLE:
        return None, None, None
    dev = int(cp.cuda.runtime.getDevice())
    key = (dev, int(n_cutoff), str(np.dtype(dtype)))
    cached = _CHAOS_KERNEL_CACHE.get(key)
    if cached is not None:
        return cached

    # Note: we pass log_n and inv_sqrt_n arrays to avoid recomputing log/sqrt in-kernel.
    code = r"""
    extern "C" __global__
    void chaos_eval(const double* t, const double* log_n, const double* inv_sqrt_n,
                    const int n_cutoff, double* out_f, double* out_fp, const int n) {
        int i = (int)(blockDim.x * blockIdx.x + threadIdx.x);
        if (i >= n) return;
        double ti = t[i];
        // theta(t) = (t/2) * log(t/(2*pi)) - (t/2) - pi/8
        // dtheta/dt = 0.5 * log(t/(2*pi))
        const double two_pi = 6.283185307179586476925286766559;
        double log_term = log(ti / two_pi);
        double theta = 0.5 * ti * log_term - 0.5 * ti - 0.39269908169872415480783042290993786; // pi/8
        double d_theta = 0.5 * log_term;

        double acc_f = 0.0;
        double acc_fp = 0.0;
        #pragma unroll
        for (int j = 0; j < n_cutoff; ++j) {
            double ln = log_n[j];
            double invs = inv_sqrt_n[j];
            double arg = theta - ti * ln;
            double c = cos(arg);
            double s = sin(arg);
            acc_f += c * invs;
            acc_fp += (-s) * (d_theta - ln) * invs;
        }
        out_f[i] = 2.0 * acc_f;
        out_fp[i] = 2.0 * acc_fp;
    }
    """
    kernel = cp.RawKernel(code, "chaos_eval", options=("--std=c++14",), backend="nvrtc")
    log_n, inv_sqrt_n = _get_chaos_tables_cupy(n_cutoff=n_cutoff, dtype=np.float64)
    out = (kernel, log_n, inv_sqrt_n)
    _CHAOS_KERNEL_CACHE[key] = out
    return out


def sample_gpu_utilization_percent(samples=3, interval_sec=0.1):
    """
    Sample GPU utilization (%) using nvidia-smi.
    Returns float average utilization, or None if unavailable.
    """
    vals = []
    for _ in range(max(1, int(samples))):
        try:
            out = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            # First GPU only
            if out:
                v = float(out.splitlines()[0].strip())
                vals.append(v)
        except Exception:
            return None
        if interval_sec and interval_sec > 0:
            time.sleep(float(interval_sec))
    if not vals:
        return None
    return float(sum(vals) / len(vals))


def _run_nvidia_smi_query(args):
    """
    Run a nvidia-smi query command and return stdout string, or None if unavailable.
    args: list of command arguments after 'nvidia-smi'.
    """
    try:
        out = subprocess.check_output(["nvidia-smi", *args], stderr=subprocess.DEVNULL, text=True).strip()
        return out if out else None
    except Exception:
        return None


def get_gpu_device_info():
    """
    Return a dict of GPU/backend info for logging.
    Works best with CuPy; falls back to minimal info if not available.
    """
    info = {
        "pid": int(os.getpid()),
        "python": sys.version.split()[0],
        "numpy": getattr(np, "__version__", "unknown"),
        "cupy_available": bool(_CUPY_AVAILABLE),
        "cupy": getattr(cp, "__version__", None) if _CUPY_AVAILABLE else None,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "backend": "CuPy (GPU)" if _CUPY_AVAILABLE else "NumPy (CPU fallback)",
        "gpu_index": None,
        "gpu_name": None,
        "gpu_cc": None,
        "gpu_mem_total_mb": None,
    }

    if _CUPY_AVAILABLE:
        try:
            dev = int(cp.cuda.runtime.getDevice())
            info["gpu_index"] = dev
            props = cp.cuda.runtime.getDeviceProperties(dev)
            # props is a dict-like object
            info["gpu_name"] = props.get("name", b"").decode("utf-8", errors="replace") if isinstance(props.get("name"), (bytes, bytearray)) else props.get("name")
            info["gpu_cc"] = f'{props.get("major")}.{props.get("minor")}'
            total_mem = props.get("totalGlobalMem")
            if total_mem:
                info["gpu_mem_total_mb"] = float(total_mem) / (1024 ** 2)
        except Exception:
            pass
    return info


def query_gpu_memory_and_util(gpu_index=None):
    """
    Query GPU memory.used, memory.total, utilization.gpu for a given GPU index via nvidia-smi.
    Returns dict with keys: mem_used_mb, mem_total_mb, util_percent; missing values are None.
    """
    out = _run_nvidia_smi_query(
        [
            "--query-gpu=index,memory.used,memory.total,utilization.gpu",
            "--format=csv,noheader,nounits",
            *([] if gpu_index is None else ["-i", str(int(gpu_index))]),
        ]
    )
    if not out:
        return {"mem_used_mb": None, "mem_total_mb": None, "util_percent": None}
    # If multiple GPUs returned, take first line.
    line = out.splitlines()[0].strip()
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 4:
        return {"mem_used_mb": None, "mem_total_mb": None, "util_percent": None}
    try:
        return {
            "mem_used_mb": float(parts[1]),
            "mem_total_mb": float(parts[2]),
            "util_percent": float(parts[3]),
        }
    except Exception:
        return {"mem_used_mb": None, "mem_total_mb": None, "util_percent": None}


def query_process_gpu_memory_mb(pid=None):
    """
    Query this process GPU memory usage (MB) via nvidia-smi compute apps.
    Returns float MB (sum across GPUs) or None if nvidia-smi query not available.
    """
    pid = int(os.getpid()) if pid is None else int(pid)
    out = _run_nvidia_smi_query(["--query-compute-apps=pid,used_memory", "--format=csv,noheader,nounits"])
    if out is None:
        return None
    total = 0.0
    found = False
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2:
            continue
        try:
            lp = int(parts[0])
            if lp != pid:
                continue
            mem = float(parts[1])
            total += mem
            found = True
        except Exception:
            continue
    return total if found else 0.0


def riemann_n_formula(t, n, xp):
    """Riemann-von Mangoldt formula inverse: f(t,n) = 0 at n-th zero.
    Vectorized over arrays t and n (same shape)."""
    two_pi = xp.pi * 2.0
    val = (t / two_pi) * xp.log(t / two_pi) - (t / two_pi) + 0.875
    return val - n


def riemann_n_formula_derivative(t, xp):
    """Derivative of riemann_n_formula w.r.t. t (n constant).
    d/dt [ (t/(2*pi))*log(t/(2*pi)) - t/(2*pi) ] = (1/(2*pi))*log(t/(2*pi))."""
    two_pi = xp.pi * 2.0
    return (1.0 / two_pi) * xp.log(t / two_pi)


def riemann_siegel_theta(t, xp):
    """Riemann-Siegel theta function. Vectorized over t."""
    two_pi = xp.pi * 2.0
    return (t / 2.0) * xp.log(t / two_pi) - (t / 2.0) - (xp.pi / 8.0)


def riemann_siegel_theta_derivative(t, xp):
    """Derivative of Riemann-Siegel theta w.r.t. t."""
    two_pi = xp.pi * 2.0
    return 0.5 * xp.log(t / two_pi)


def chaos_wave_eval(t, n_cutoff, xp):
    """
    Return (f, fp) for chaos wave at t, where:
      f  = chaos_wave_function(t)
      fp = d/dt chaos_wave_function(t)
    Uses a single custom CUDA kernel for CuPy to reduce temporaries and improve GPU utilization.
    """
    t = xp.asarray(t, dtype=float)
    if t.ndim == 0:
        t = t[None]

    if xp.__name__ == "cupy":
        kernel, log_n, inv_sqrt_n = _get_chaos_kernel_and_tables(n_cutoff=n_cutoff, dtype=np.float64)
        out_f = cp.empty_like(t, dtype=cp.float64)
        out_fp = cp.empty_like(t, dtype=cp.float64)
        n = int(t.size)
        threads = 256
        blocks = (n + threads - 1) // threads
        kernel((blocks,), (threads,), (t, log_n, inv_sqrt_n, int(n_cutoff), out_f, out_fp, n))
        return out_f, out_fp

    # NumPy fallback (vectorized)
    theta = riemann_siegel_theta(t, xp)
    d_theta = riemann_siegel_theta_derivative(t, xp)
    n_vec = xp.arange(1, n_cutoff + 1, dtype=float)
    log_n = xp.log(n_vec)
    sqrt_n = xp.sqrt(n_vec)
    arg = theta[:, None] - t[:, None] * log_n[None, :]
    inv_sqrt = 1.0 / sqrt_n[None, :]
    f = 2.0 * (xp.cos(arg) * inv_sqrt).sum(axis=1)
    fp = 2.0 * ((-xp.sin(arg)) * (d_theta[:, None] - log_n[None, :]) * inv_sqrt).sum(axis=1)
    return f, fp


def batched_macro(n_array, xp, max_iter=20, tol=1e-12):
    """Batched macroscopic prediction: solve riemann_n_formula(t, n) = 0 for all n.
    Returns array of t_macro same shape as n_array."""
    two_pi = float(np.pi * 2.0)
    # Initial guess: t0 = 2*pi*n / log(n)
    nf = xp.asarray(n_array, dtype=float)
    t = xp.where(nf > 1, two_pi * nf / xp.log(nf), 14.0)
    for _ in range(max_iter):
        f = riemann_n_formula(t, nf, xp)
        fp = riemann_n_formula_derivative(t, xp)
        # Avoid division by zero
        step = f / (fp + 1e-14)
        t = t - step
        if xp.abs(step).max() < tol:
            break
    return t


def batched_micro(t_macro, n_array, stiffness, xp):
    """Batched microscopic correction using theoretical previous zero.
    Uses t_macro[n-1] as approximation for previous_zero to keep parallelism."""
    nf = xp.asarray(n_array, dtype=float)
    # Theoretical location for n-1 (for correction)
    n_prev = xp.maximum(nf - 1, 1)
    two_pi = float(np.pi * 2.0)
    t0_prev = xp.where(n_prev > 1, two_pi * n_prev / xp.log(n_prev), 14.0)
    t_prev_theory = batched_macro(n_prev, xp, max_iter=15, tol=1e-10)
    # Previous prediction: use t_macro of previous index (shift)
    t_prev_pred = xp.roll(t_macro, 1)
    # First index in batch has no previous zero -> use t_prev_theory so correction = 0
    t_prev_pred = xp.where(xp.arange(nf.size, dtype=xp.int32) > 0, t_prev_pred, t_prev_theory)
    # For n=1 no correction
    t_prev_pred = xp.where(nf > 1, t_prev_pred, t_prev_theory)
    displacement = t_prev_pred - t_prev_theory
    correction = displacement * stiffness
    return t_macro + correction


def batched_chaos_refinement(t_micro, n_cutoff, xp, search_window=0.5, max_iter=15, tol=1e-10):
    """Batched Newton refinement: find root of chaos_wave_function near t_micro."""
    t = xp.asarray(t_micro, dtype=float) + 0.0  # ensure copy for in-place updates
    for _ in range(max_iter):
        f, fp = chaos_wave_eval(t, n_cutoff, xp)
        step = f / (xp.abs(fp) + 1e-14)
        t = t - step
        # Clamp to window around original t_micro
        t = xp.clip(t, t_micro - search_window, t_micro + search_window)
        if xp.abs(step).max() < tol:
            break
    return t


def predict_zero_three_step_batched(n_array, stiffness=0.95, n_cutoff=20, xp=None):
    """
    Three-step prediction for a batch of zero indices (GPU-optimized).
    Uses theoretical previous zero for microscopic step to allow full batching.
    """
    if xp is None:
        xp = _get_array_module(use_gpu=True)
    n_array = xp.asarray(n_array, dtype=float)
    t_macro = batched_macro(n_array, xp)
    t_micro = batched_micro(t_macro, n_array, stiffness, xp)
    t_final = batched_chaos_refinement(t_micro, n_cutoff, xp)
    return t_final


def test_scalability_gpu(
    start_n=1000,
    end_n=10000,
    step=100,
    batch_size=500,
    use_gpu=True,
    use_dynamic_memory=True,
    reserve_ratio=0.2,
    double_buffer=False,
    streams=2,
    collect_results=True,
    print_details=True,
):
    """
    Test algorithm scalability on GPU with batched computation.
    use_dynamic_memory: cap batch_size by GPU free memory (CuPy only).
    double_buffer: overlap GPU compute of batch b with CPU copy/result-build of batch b-1 (CuPy only).
    """
    xp = _get_array_module(use_gpu)
    backend = "CuPy (GPU)" if xp.__name__ == "cupy" else "NumPy (CPU fallback)"
    n_cutoff = 20

    # Dynamic GPU memory: cap batch_size by safe value
    if use_gpu and _CUPY_AVAILABLE and use_dynamic_memory:
        safe_batch, free_mb, total_mb = get_gpu_safe_batch_size(n_cutoff=n_cutoff, reserve_ratio=reserve_ratio)
        if safe_batch is not None and free_mb > 0:
            orig_batch = batch_size
            batch_size = min(batch_size, safe_batch)
            if print_details:
                if batch_size < orig_batch:
                    print(
                        f"Dynamic GPU memory: capped batch_size {orig_batch} -> {batch_size} "
                        f"(free {free_mb:.0f} MB, reserve {reserve_ratio*100:.0f}%)"
                    )
                else:
                    print(f"Dynamic GPU memory: free {free_mb:.0f} / {total_mb:.0f} MB, safe_batch up to {safe_batch}")

    if print_details:
        print(f"Scalability test (GPU-optimized) — backend: {backend}")
        print(f"Testing zeros {start_n} to {end_n} (step={step}), batch_size={batch_size}")
        if double_buffer and xp.__name__ == "cupy":
            print(f"Streamed pipeline (CPU/GPU overlap): enabled, streams={streams}")
        print("=" * 60)

    n_values = list(range(int(start_n), int(end_n) + 1, int(step)))
    if not n_values:
        print("No indices to test.")
        return []

    results = [] if collect_results else None
    total_time = 0.0
    total_zeros = 0
    sum_error = 0.0
    max_error = 0.0
    n_batches = (len(n_values) + batch_size - 1) // batch_size
    use_overlap = double_buffer and xp.__name__ == "cupy" and n_batches >= 2 and int(streams) >= 2

    if use_overlap:
        stream_count = min(int(streams), n_batches)
        stream_list = [cp.cuda.Stream() for _ in range(stream_count)]
        # Per-stream last submitted batch
        last_pred = [None] * stream_count
        last_theory = [None] * stream_count
        last_n_batch = [None] * stream_count
        last_i0 = [0] * stream_count
        last_i1 = [0] * stream_count
        last_elapsed = [0.0] * stream_count

    for b in range(n_batches):
        start_time = time.perf_counter()
        i0 = b * batch_size
        i1 = min(i0 + batch_size, len(n_values))
        n_batch = n_values[i0:i1]
        n_arr = xp.asarray(n_batch, dtype=float)

        if use_overlap:
            si = b % stream_count
            stream = stream_list[si]
            # If this stream already has a previous batch, harvest it now (sync -> copy -> append)
            if last_pred[si] is not None:
                stream.synchronize()
                batch_len = (last_i1[si] - last_i0[si])
                total_zeros += batch_len
                per_zero_ms = (last_elapsed[si] / batch_len) * 1000
                # Error on GPU, copy scalars only
                err = cp.abs(last_pred[si] - last_theory[si]) / (cp.abs(last_theory[si]) + 1e-14)
                err_mean = float(cp.asnumpy(err.mean()))
                err_max = float(cp.asnumpy(err.max()))
                sum_error += err_mean * batch_len
                max_error = max(max_error, err_max)
                if collect_results:
                    pred_cpu = cp.asnumpy(last_pred[si])
                    t_theory_cpu = cp.asnumpy(last_theory[si])
                    for i, n in enumerate(last_n_batch[si]):
                        rel_err = abs(float(pred_cpu[i]) - float(t_theory_cpu[i])) / (abs(float(t_theory_cpu[i])) + 1e-14)
                        results.append({
                            "n": int(n),
                            "prediction": float(pred_cpu[i]),
                            "time_ms": per_zero_ms,
                            "estimated_error": rel_err,
                        })

            with stream:
                predictions = predict_zero_three_step_batched(n_arr, stiffness=0.95, n_cutoff=n_cutoff, xp=xp)
                t_theory_batch = batched_macro(n_arr, xp, max_iter=15, tol=1e-10)

            elapsed = time.perf_counter() - start_time
            total_time += elapsed
            last_pred[si] = predictions
            last_theory[si] = t_theory_batch
            last_n_batch[si] = n_batch
            last_i0[si] = i0
            last_i1[si] = i1
            last_elapsed[si] = elapsed
        else:
            predictions = predict_zero_three_step_batched(n_arr, stiffness=0.95, n_cutoff=n_cutoff, xp=xp)
            t_theory_batch = batched_macro(n_arr, xp, max_iter=15, tol=1e-10)
            elapsed = time.perf_counter() - start_time
            total_time += elapsed

            batch_len = (i1 - i0)
            total_zeros += batch_len
            per_zero_ms = (elapsed / batch_len) * 1000
            if xp.__name__ == "cupy":
                cp.cuda.Stream.null.synchronize()
                err = cp.abs(predictions - t_theory_batch) / (cp.abs(t_theory_batch) + 1e-14)
                err_mean = float(cp.asnumpy(err.mean()))
                err_max = float(cp.asnumpy(err.max()))
            else:
                pred_cpu = np.asarray(predictions)
                t_theory_cpu = np.asarray(t_theory_batch)
                err = np.abs(pred_cpu - t_theory_cpu) / (np.abs(t_theory_cpu) + 1e-14)
                err_mean = float(np.mean(err))
                err_max = float(np.max(err))
            sum_error += err_mean * batch_len
            max_error = max(max_error, err_max)

            if collect_results:
                if xp.__name__ == "cupy":
                    pred_cpu = cp.asnumpy(predictions)
                    t_theory_cpu = cp.asnumpy(t_theory_batch)
                for i, n in enumerate(n_batch):
                    rel_err = abs(float(pred_cpu[i]) - float(t_theory_cpu[i])) / (abs(float(t_theory_cpu[i])) + 1e-14)
                    results.append({
                        "n": int(n),
                        "prediction": float(pred_cpu[i]),
                        "time_ms": per_zero_ms,
                        "estimated_error": rel_err,
                    })

        if print_details and ((b + 1) % max(1, n_batches // 5) == 0 or b == n_batches - 1):
            elapsed_print = elapsed if not use_overlap else (time.perf_counter() - start_time)
            done = (len(results) if collect_results else total_zeros)
            print(f"  Batch {b + 1}/{n_batches} ({done} tests) — {elapsed_print:.3f}s")
    if use_overlap:
        # Harvest remaining batches from all streams
        for si, stream in enumerate(stream_list):
            if last_pred[si] is None:
                continue
            stream.synchronize()
            batch_len = (last_i1[si] - last_i0[si])
            total_zeros += batch_len
            per_zero_ms = (last_elapsed[si] / batch_len) * 1000
            err = cp.abs(last_pred[si] - last_theory[si]) / (cp.abs(last_theory[si]) + 1e-14)
            err_mean = float(cp.asnumpy(err.mean()))
            err_max = float(cp.asnumpy(err.max()))
            sum_error += err_mean * batch_len
            max_error = max(max_error, err_max)
            if collect_results:
                pred_cpu = cp.asnumpy(last_pred[si])
                t_theory_cpu = cp.asnumpy(last_theory[si])
                for i, n in enumerate(last_n_batch[si]):
                    rel_err = abs(float(pred_cpu[i]) - float(t_theory_cpu[i])) / (abs(float(t_theory_cpu[i])) + 1e-14)
                    results.append({
                        "n": int(n),
                        "prediction": float(pred_cpu[i]),
                        "time_ms": per_zero_ms,
                        "estimated_error": rel_err,
                    })

    if collect_results:
        times = [r["time_ms"] for r in results]
        errors = [r["estimated_error"] for r in results]
    else:
        times = None
        errors = None

    mean_error = (sum_error / total_zeros) if total_zeros else 0.0
    mean_ms_per_zero = (total_time / total_zeros) * 1000 if total_zeros else 0.0

    if print_details:
        print("\n" + "=" * 60)
        print("SCALABILITY TEST RESULTS (GPU)")
        print("=" * 60)
        print(f"Backend: {backend}")
        print(f"Total zeros tested: {total_zeros if not collect_results else len(results)}")
        print(f"Range: {start_n} to {end_n}, batch_size: {batch_size}")
        print(f"\nTiming (per zero):")
        if collect_results:
            print(f"  Mean: {np.mean(times):.2f} ms")
            print(f"  Median: {np.median(times):.2f} ms")
            print(f"  Min: {np.min(times):.2f} ms")
            print(f"  Max: {np.max(times):.2f} ms")
        else:
            print(f"  Mean: {mean_ms_per_zero:.2f} ms")
        print(f"  Total time: {total_time:.2f} s")
        print(f"\nError (relative):")
        if collect_results:
            print(f"  Mean: {np.mean(errors) * 100:.4f}%")
            print(f"  Median: {np.median(errors) * 100:.4f}%")
            print(f"  Max: {np.max(errors) * 100:.4f}%")
        else:
            print(f"  Mean: {mean_error * 100:.4f}%")
            print(f"  Max: {max_error * 100:.4f}%")

    if collect_results:
        return results
    return {
        "backend": backend,
        "start_n": int(start_n),
        "end_n": int(end_n),
        "step": int(step),
        "batch_size": int(batch_size),
        "zeros": int(total_zeros),
        "total_time_sec": float(total_time),
        "mean_ms_per_zero": float(mean_ms_per_zero),
        "mean_error": float(mean_error),
        "max_error": float(max_error),
    }


def run_for_duration(
    duration_seconds,
    output_path,
    start_n=1000,
    end_n=10000,
    step=100,
    batch_size=500,
    use_dynamic_memory=True,
    reserve_ratio=0.2,
    double_buffer=False,
    streams=2,
    util_max_percent=87.0,
    util_samples=3,
    util_interval_sec=0.1,
    log_interval_sec=10.0,
    max_sleep_sec=2.0,
):
    """
    Run scalability tests until duration_seconds has elapsed.
    Logging is lightweight: periodic one-line summaries (log_interval_sec) + final summary.
    Utilization cap: if sampled GPU util > util_max_percent, sleep briefly to reduce duty cycle.
    """
    terminal_out = sys.stdout
    f = None
    if output_path:
        f = open(output_path, "w", encoding="utf-8")

    def log_line(s):
        # Always report on running terminal, and also write to output file if provided.
        try:
            print(s, file=terminal_out, flush=True)
        except Exception:
            pass
        if f is not None:
            f.write(str(s) + "\n")
            f.flush()
    try:
        dev_info = get_gpu_device_info()
        log_line("GPU Scalability Test — duration run (light logging + util cap)")
        log_line(f"Started: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')} UTC")
        log_line(f"Target duration: {duration_seconds} s ({duration_seconds / 3600:.2f} hours)")
        log_line(f"Output file: {output_path or '(none; terminal only)'}")
        log_line(
            f"Backend: {dev_info.get('backend')} | pid={dev_info.get('pid')} | "
            f"python={dev_info.get('python')} numpy={dev_info.get('numpy')} cupy={dev_info.get('cupy') or 'n/a'}"
        )
        if dev_info.get("cuda_visible_devices") != "":
            log_line(f"CUDA_VISIBLE_DEVICES={dev_info.get('cuda_visible_devices')}")
        if dev_info.get("gpu_index") is not None:
            log_line(
                f"GPU device: index={dev_info.get('gpu_index')} name={dev_info.get('gpu_name') or 'unknown'} "
                f"cc={dev_info.get('gpu_cc') or 'unknown'} mem_total_mb={dev_info.get('gpu_mem_total_mb') or 'unknown'}"
            )
        log_line(f"Util cap: {util_max_percent:.1f}%  (samples={util_samples}, interval={util_interval_sec}s)")
        log_line(f"Log interval: {log_interval_sec:.1f}s")
        log_line("=" * 60)

        end_time = time.perf_counter() + duration_seconds
        run_count = 0
        total_zeros = 0
        sum_time_sec = 0.0
        sum_error = 0.0
        max_error = 0.0
        sum_util = 0.0
        util_count = 0
        last_log_t = time.perf_counter()
        last_logged_runs = 0
        last_logged_zeros = 0
        last_logged_time = 0.0
        last_logged_error = 0.0
        last_logged_sleep = 0.0

        while time.perf_counter() < end_time:
            run_count += 1
            run_start = time.perf_counter()
            summary = test_scalability_gpu(
                start_n=start_n,
                end_n=end_n,
                step=step,
                batch_size=batch_size,
                use_gpu=True,
                use_dynamic_memory=use_dynamic_memory,
                reserve_ratio=reserve_ratio,
                double_buffer=double_buffer,
                streams=streams,
                collect_results=False,
                print_details=False,
            )
            run_elapsed = time.perf_counter() - run_start
            zeros = int(summary["zeros"])
            total_zeros += zeros
            sum_time_sec += float(summary["total_time_sec"])
            sum_error += float(summary["mean_error"]) * zeros
            max_error = max(max_error, float(summary["max_error"]))

            util = sample_gpu_utilization_percent(samples=util_samples, interval_sec=util_interval_sec)
            # Duty-cycle pacing: even without reliable SMI util sampling, keep compute duty cycle <= util_max_percent.
            sleep_s = 0.0
            if util_max_percent and util_max_percent > 0:
                sleep_s = max(0.0, (100.0 / float(util_max_percent)) - 1.0) * max(0.0, run_elapsed)
            if util is not None:
                sum_util += util
                util_count += 1
                if util_max_percent and util > util_max_percent:
                    # Duty-cycle throttle: sleep proportional to overflow
                    ratio = (util / util_max_percent) - 1.0
                    sleep_s = min(float(max_sleep_sec), sleep_s + max(0.0, ratio * max(0.05, run_elapsed)))
            if sleep_s > 0:
                time.sleep(min(float(max_sleep_sec), sleep_s))
            last_logged_sleep += sleep_s

            now = time.perf_counter()
            if (now - last_log_t) >= float(log_interval_sec):
                runs_delta = run_count - last_logged_runs
                zeros_delta = total_zeros - last_logged_zeros
                time_delta = sum_time_sec - last_logged_time
                err_delta = sum_error - last_logged_error
                avg_ms = (time_delta / max(1, zeros_delta)) * 1000
                avg_err = (err_delta / max(1, zeros_delta)) * 100
                avg_util = (sum_util / util_count) if util_count else float("nan")
                remaining = end_time - now
                proc_gpu_mem_mb = query_process_gpu_memory_mb(pid=dev_info.get("pid"))
                gpu_stats = query_gpu_memory_and_util(gpu_index=dev_info.get("gpu_index"))
                proc_mem_str = "n/a" if proc_gpu_mem_mb is None else f"{proc_gpu_mem_mb:.0f}"
                gpu_mem_used_str = "n/a" if gpu_stats.get("mem_used_mb") is None else f"{gpu_stats.get('mem_used_mb'):.0f}/{gpu_stats.get('mem_total_mb'):.0f}"
                log_line(
                    f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')} "
                    f"backend={'cupy' if _CUPY_AVAILABLE else 'numpy'} "
                    f"runs={run_count} (+{runs_delta}) zeros={total_zeros} (+{zeros_delta}) "
                    f"ms/zero={avg_ms:.3f} err_mean%={avg_err:.4f} err_max%={max_error*100:.4f} "
                    f"gpu_util%~={avg_util:.1f} gpu_mem_mb={gpu_mem_used_str} proc_gpu_mem_mb={proc_mem_str} "
                    f"sleep_added={last_logged_sleep:.2f}s rem={remaining:.0f}s"
                )
                # Reset interval baselines
                last_log_t = now
                last_logged_runs = run_count
                last_logged_zeros = total_zeros
                last_logged_time = sum_time_sec
                last_logged_error = sum_error
                last_logged_sleep = 0.0

            if time.perf_counter() >= end_time:
                break

        log_line("\n" + "=" * 60)
        log_line("DURATION RUN SUMMARY")
        log_line("=" * 60)
        log_line(f"Total runs: {run_count}")
        log_line(f"Total zeros tested: {total_zeros}")
        log_line(f"Target duration: {duration_seconds} s")
        log_line(f"Finished: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')} UTC")
        if total_zeros > 0:
            mean_ms = (sum_time_sec / total_zeros) * 1000
            mean_err = (sum_error / total_zeros) * 100
            avg_util = (sum_util / util_count) if util_count else float("nan")
            log_line(f"\nAggregate timing (per zero): mean {mean_ms:.3f} ms")
            log_line(f"Aggregate error (relative): mean {mean_err:.4f}%  max {max_error*100:.4f}%")
            log_line(f"GPU util sampled avg: {avg_util:.1f}%  (samples={util_count})")
        log_line("=" * 60)
        log_line("GPU scalability duration run completed.")
    finally:
        if output_path and f is not None:
            f.close()
    return {
        "runs": int(run_count),
        "zeros": int(total_zeros),
        "mean_ms_per_zero": float((sum_time_sec / total_zeros) * 1000) if total_zeros else 0.0,
        "mean_error_percent": float((sum_error / total_zeros) * 100) if total_zeros else 0.0,
        "max_error_percent": float(max_error * 100),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPU scalability test for zero prediction.")
    parser.add_argument("--duration", type=float, default=0, help="Run until this many seconds elapsed (e.g. 10800 for 3 hours).")
    parser.add_argument("--output", type=str, default="", help="Write output to this file (used with --duration).")
    parser.add_argument("--start-n", type=int, default=1000, help="Start zero index (default 1000).")
    parser.add_argument("--end-n", type=int, default=10000, help="End zero index (default 10000).")
    parser.add_argument("--step", type=int, default=100, help="Step between zeros (default 100).")
    parser.add_argument("--batch-size", type=int, default=500, help="Batch size (default 500).")
    parser.add_argument("--no-dynamic-memory", action="store_true", help="Disable dynamic GPU memory cap.")
    parser.add_argument("--reserve-ratio", type=float, default=0.2, help="Fraction of GPU free memory to reserve (default 0.2).")
    parser.add_argument("--double-buffer", action="store_true", help="Overlap GPU compute with CPU copy/result-build (two streams).")
    parser.add_argument("--streams", type=int, default=2, help="Number of CuPy streams for pipelined parallel batches (default 2).")
    parser.add_argument(
        "--util-max",
        type=float,
        default=87.0,
        help="Max utilization target for duration pacing (default 87). Implemented as duty-cycle cap (sleep between runs).",
    )
    parser.add_argument("--util-samples", type=int, default=3, help="Samples for util averaging (default 3).")
    parser.add_argument("--util-interval-sec", type=float, default=0.1, help="Seconds between util samples (default 0.1).")
    parser.add_argument("--log-interval-sec", type=float, default=10.0, help="Seconds between log lines in duration run (default 10).")
    parser.add_argument("--max-sleep-sec", type=float, default=2.0, help="Max sleep per run for util pacing (default 2).")
    args = parser.parse_args()

    if not _CUPY_AVAILABLE:
        print("CuPy not found. Install with: pip install cupy-cuda12x")
        print("Running with NumPy (CPU) fallback.\n")

    if args.duration > 0:
        duration_sec = int(args.duration)
        if args.output:
            output_path = args.output
        else:
            output_path = f"06_docs/gpu_scalability_3h_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.txt"
        run_for_duration(
            duration_sec,
            output_path,
            start_n=args.start_n,
            end_n=args.end_n,
            step=args.step,
            batch_size=args.batch_size,
            use_dynamic_memory=not args.no_dynamic_memory,
            reserve_ratio=args.reserve_ratio,
            double_buffer=args.double_buffer,
            streams=args.streams,
            util_max_percent=args.util_max,
            util_samples=args.util_samples,
            util_interval_sec=args.util_interval_sec,
            log_interval_sec=args.log_interval_sec,
            max_sleep_sec=args.max_sleep_sec,
        )
    else:
        results = test_scalability_gpu(
            start_n=args.start_n,
            end_n=args.end_n,
            step=args.step,
            batch_size=args.batch_size,
            use_gpu=True,
            use_dynamic_memory=not args.no_dynamic_memory,
            reserve_ratio=args.reserve_ratio,
            double_buffer=args.double_buffer,
            streams=args.streams,
        )
        print("\n" + "=" * 60)
        print("GPU scalability test completed.")
