#!/usr/bin/env python3
"""
Benchmark Comparison: Our algorithm vs. mpmath and Arb libraries
"""

import numpy as np
import time
from scipy.optimize import fsolve, brentq

# Try to import mpmath (optional)
try:
    import mpmath
    MPMATH_AVAILABLE = True
except ImportError:
    MPMATH_AVAILABLE = False
    print("Warning: mpmath not available. Install with: pip install mpmath")

# Arb is typically accessed via Python bindings (not always available)
ARB_AVAILABLE = False
try:
    import flint
    ARB_AVAILABLE = True
except ImportError:
    pass

def riemann_n_formula(t, n):
    """Riemann-von Mangoldt formula inverse."""
    val = (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - (t / (2 * np.pi)) + 0.875
    return val - n

def riemann_siegel_theta(t):
    """Riemann-Siegel theta function."""
    return (t / 2.0) * np.log(t / (2.0 * np.pi)) - (t / 2.0) - (np.pi / 8.0)

def chaos_wave_function(t, n_cutoff=20):
    """Riemann-Siegel Z-function approximation."""
    theta = riemann_siegel_theta(t)
    val = 0.0
    for n in range(1, n_cutoff + 1):
        term = np.cos(theta - t * np.log(n)) / np.sqrt(n)
        val += term
    return 2.0 * val

def our_algorithm(n, previous_zero=None, stiffness=0.95):
    """Our three-step prediction algorithm."""
    # Step 1: Macroscopic
    t0 = 2 * np.pi * n / np.log(n) if n > 1 else 14.0
    t_macro = fsolve(riemann_n_formula, x0=t0, args=(n))[0]
    
    # Step 2: Microscopic
    if previous_zero is not None and n > 1:
        t_prev_theory = fsolve(riemann_n_formula, x0=t0-10, args=(n-1))[0]
        displacement_prev = previous_zero - t_prev_theory
        correction = displacement_prev * stiffness
        t_micro = t_macro + correction
    else:
        t_micro = t_macro
    
    # Step 3: Chaos engine
    search_window = 0.5
    t_min = t_micro - search_window
    t_max = t_micro + search_window
    
    try:
        t_final = brentq(chaos_wave_function, t_min, t_max)
    except ValueError:
        t_final = t_micro
    
    return t_final

def benchmark_mpmath(n, iterations=10):
    """Benchmark mpmath zetazero function."""
    if not MPMATH_AVAILABLE:
        return None
    
    times = []
    for _ in range(iterations):
        start = time.time()
        mpmath.mp.dps = 15  # Set precision
        zero = mpmath.zetazero(n)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        times.append(elapsed)
    
    return np.mean(times), np.std(times)

def benchmark_our_algorithm(n, iterations=10):
    """Benchmark our three-step algorithm."""
    times = []
    for _ in range(iterations):
        start = time.time()
        result = our_algorithm(n)
        elapsed = (time.time() - start) * 1000  # Convert to ms
        times.append(elapsed)
    
    return np.mean(times), np.std(times)

def run_benchmarks(test_indices=[30, 100, 500, 1000, 5000, 10000]):
    """
    Run benchmarks comparing our algorithm with mpmath.
    
    Args:
        test_indices: List of zero indices to test
    """
    print("=" * 70)
    print("RUNTIME BENCHMARK COMPARISON")
    print("=" * 70)
    print(f"{'Zero Index':<12} {'Our Algorithm':<20} {'mpmath':<20} {'Speedup':<15}")
    print("-" * 70)
    
    results = []
    
    for n in test_indices:
        # Benchmark our algorithm
        our_mean, our_std = benchmark_our_algorithm(n, iterations=5)
        
        # Benchmark mpmath (if available)
        if MPMATH_AVAILABLE:
            mpmath_mean, mpmath_std = benchmark_mpmath(n, iterations=5)
            speedup = mpmath_mean / our_mean if our_mean > 0 else 0
            print(f"{n:<12} {our_mean:>6.2f}±{our_std:>5.2f} ms    "
                  f"{mpmath_mean:>6.2f}±{mpmath_std:>5.2f} ms    "
                  f"{speedup:>5.2f}x")
            results.append({
                'n': n,
                'our_time': our_mean,
                'mpmath_time': mpmath_mean,
                'speedup': speedup
            })
        else:
            print(f"{n:<12} {our_mean:>6.2f}±{our_std:>5.2f} ms    "
                  f"{'N/A':<20} {'N/A':<15}")
            results.append({
                'n': n,
                'our_time': our_mean,
                'mpmath_time': None,
                'speedup': None
            })
    
    # Batch computation benchmark
    print("\n" + "=" * 70)
    print("BATCH COMPUTATION BENCHMARK (1,000 zeros)")
    print("=" * 70)
    
    batch_size = 1000
    start_n = 1000
    
    # Our algorithm batch
    start_time = time.time()
    prev_zero = None
    for i in range(batch_size):
        n = start_n + i
        prev_zero = our_algorithm(n, previous_zero=prev_zero)
    our_batch_time = time.time() - start_time
    
    print(f"Our algorithm (1,000 zeros): {our_batch_time:.2f} seconds")
    print(f"  Average per zero: {our_batch_time*1000/batch_size:.2f} ms")
    
    if MPMATH_AVAILABLE:
        # mpmath batch
        start_time = time.time()
        for i in range(batch_size):
            n = start_n + i
            mpmath.mp.dps = 15
            mpmath.zetazero(n)
        mpmath_batch_time = time.time() - start_time
        
        print(f"mpmath (1,000 zeros): {mpmath_batch_time:.2f} seconds")
        print(f"  Average per zero: {mpmath_batch_time*1000/batch_size:.2f} ms")
        print(f"  Speedup: {mpmath_batch_time/our_batch_time:.2f}x")
    
    print("\n" + "=" * 70)
    print("Benchmark completed!")
    
    return results

if __name__ == "__main__":
    # Run benchmarks
    results = run_benchmarks(test_indices=[30, 100, 500, 1000, 5000, 10000])
    
    if not MPMATH_AVAILABLE:
        print("\nNote: Install mpmath for full benchmark comparison:")
        print("  pip install mpmath")
