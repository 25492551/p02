# GPU Scalability Test — Low GPU Utilization Analysis

**Date**: 2026-02-05  
**Script**: `03_script/16_scalability_test_gpu.py`

## 1. Why GPU Uses Only a Small Part of Resources

### 1.1 Small problem size per batch
- **Current run**: zeros 1,000–10,000 with step 100 → **91 values** per run.
- Batch size is 500 but we only have 91 indices, so **one batch of 91 elements**.
- GPUs are built for hundreds of thousands to millions of elements; 91 elements leave most cores idle.

### 1.2 Python loops in the hot path
- `chaos_wave_function(t, n_cutoff, xp)` and `chaos_wave_derivative(...)` use a **Python `for n in range(1, n_cutoff+1)`** (n_cutoff=20).
- Each iteration does one small array op (cos/sin, sqrt, etc.), so **20 separate kernel launches** per call instead of one large vectorized kernel.
- Many small launches cause:
  - High launch overhead.
  - CPU-GPU round-trips.
  - Underutilization of GPU parallelism.

### 1.3 Per-batch synchronization
- After each batch: `cp.cuda.Stream.null.synchronize()`.
- CPU waits for GPU to finish before starting the next batch, so **no overlap** of compute and host-side work.

### 1.4 Per-batch CPU copy
- After each batch we call `np.asnumpy(predictions)` and a Python loop to build `results`.
- This forces a **GPU→CPU sync** every batch and adds Python overhead for small N.

### 1.5 Newton iterations are many small steps
- Macro: up to 20 Newton steps; chaos: up to 15. Each step is a small kernel (91–500 elements).
- Lots of small kernels instead of one big workload.

---

## 2. Options to Overcome Low GPU Utilization

### Option A: Increase workload size (no code change)
- Run with **much larger range** so each run has many more zeros.
- Example:
  ```bash
  python 03_script/16_scalability_test_gpu.py --start-n 1000 --end-n 500000 --step 100 --batch-size 10000
  ```
- This gives ~4,990 values per run, processed in one batch of 5000 (or multiple batches of 10000). More elements per batch → better GPU fill.

### Option B: Increase batch size
- Use `--batch-size 50000` or `100000` (and ensure `end_n - start_n` is large enough).
- Fewer, larger batches → fewer syncs and more work per kernel.

### Option C: Vectorize chaos_wave (code change)
- Replace the Python loop over `n` in `chaos_wave_function` and `chaos_wave_derivative` with **one array operation** over a 2D grid `(t.size, n_cutoff)`.
- One or two kernel launches per call instead of 20 → less launch overhead and better GPU utilization.

### Option D: Reduce synchronization
- Call `synchronize()` only once after all batches (or when building final results), not after every batch.
- Optionally use **asynchronous transfers** and CuPy streams to overlap copy and compute.

### Option E: Accumulate on GPU, copy once
- Keep predictions on GPU for all batches; build a single large array, then **one** `asnumpy()` at the end.
- Reduces GPU→CPU syncs from N_batches to 1.

### Option F: Larger n_cutoff (more work per zero)
- Increase `n_cutoff` from 20 to 50 or 100 for chaos_wave (more terms).
- Increases arithmetic per zero; helpful only if batch size is already large enough.

---

## 3. Recommended combination

1. **Use larger range and batch size** when running (Option A + B):
   - `--start-n 1000 --end-n 100000 --step 100 --batch-size 10000` (or 50000 if memory allows).
2. **Vectorize chaos_wave** (Option C) so each call does one vectorized op instead of 20 small ones.
3. **Sync and copy once per run** (Option D + E): synchronize and call `asnumpy()` after all batches, not per batch.

These changes should significantly increase GPU utilization and throughput.

---

## 4. High-utilization run example

After applying the script changes (vectorized chaos_wave, deferred sync), run with a large workload:

```bash
# Single run with 99,000 zeros (batch_size 10,000 → ~10 batches)
python 03_script/16_scalability_test_gpu.py --start-n 1000 --end-n 100000 --step 100 --batch-size 10000

# Or 3-hour duration with larger range per run (more zeros per run)
python 03_script/16_scalability_test_gpu.py --duration 10800 --output 06_docs/gpu_scalability_3h_results.txt \
  --start-n 1000 --end-n 100000 --step 100 --batch-size 10000
```

Adjust `--batch-size` (e.g. 50000) if GPU memory allows; larger batches improve utilization.

---

## 5. Dynamic GPU memory control

The script can cap `batch_size` by current GPU free memory so runs do not OOM and do not use 100% of free memory.

- **Enabled by default** when using CuPy. It queries `memGetInfo()`, estimates bytes per element for the prediction pipeline, and sets `batch_size = min(requested_batch_size, safe_batch)`.
- **Reserve ratio**: by default 20% of free memory is reserved; the rest is used to compute a safe batch size. Use `--reserve-ratio 0.3` to reserve more.
- **Disable**: `--no-dynamic-memory` to use the requested `--batch-size` as-is (risk of OOM on small GPUs).

Example:
```bash
python 03_script/16_scalability_test_gpu.py --start-n 1000 --end-n 100000 --batch-size 100000
# If free memory is low, batch_size is capped and a message is printed.
```

---

## 6. Using CPU and GPU at the same time (double-buffer overlap)

**Possibility**: Yes. The script supports overlapping **GPU compute** of batch b with **CPU copy and result-building** of batch b−1 using two CuPy streams.

- **How it works**: Two streams alternate. While stream A runs `predict_zero_three_step_batched` for batch b, the CPU can synchronize stream B (batch b−1), copy results to CPU, and build the `results` list. Then stream B is used for batch b+1, and so on.
- **When it helps**: When there are **at least two batches** and the per-batch GPU time is comparable to the CPU copy/result-build time. With many small batches, overlap can reduce total wall time.
- **Enable**: `--double-buffer`. Only applies when using CuPy and when there are at least two batches.

Example:
```bash
python 03_script/16_scalability_test_gpu.py --start-n 1000 --end-n 100000 --step 100 --batch-size 500 --double-buffer
```

**Other CPU/GPU overlap options** (not implemented): Running part of the algorithm on CPU and part on GPU in parallel is possible in principle (e.g. CPU does error aggregation while GPU does next batch), but the current bottleneck is GPU compute; the main gain is from the double-buffer overlap above.
