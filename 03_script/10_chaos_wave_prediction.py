import numpy as np
from scipy.optimize import brentq

# --- 1. Setup ---
target_zero = 101.3178
previous_prediction = 101.2945 # Value obtained from step 2 (approximately)

# --- 2. Chaos Engine: Riemann-Siegel Z-function Approximation ---
# This is the physics engine that calculates 'interference of primes'
# Where Z(t) becomes 0 is exactly the zero of the zeta function

def riemann_siegel_theta(t):
    # Phase correction function (macroscopic rotation of system)
    # theta(t) ~ (t/2) * log(t/2pi) - t/2 - pi/8
    return (t / 2.0) * np.log(t / (2.0 * np.pi)) - (t / 2.0) - (np.pi / 8.0)

def chaos_wave_function(t, n_cutoff=20):
    # Wave synthesis of primes (and integers)
    # Z(t) approx 2 * sum( cos(theta(t) - t*log(n)) / sqrt(n) )
    # n_cutoff: How many 'butterfly (prime)' wingbeats to consider?
    # These terms interfere with each other to fill the 0.02 error
    
    theta = riemann_siegel_theta(t)
    val = 0.0
    
    # Sum integer waves from 1 to N (including influence of major primes)
    for n in range(1, n_cutoff + 1):
        term = np.cos(theta - t * np.log(n)) / np.sqrt(n)
        val += term
        
    return 2.0 * val

# --- 3. Precise Strike (Root Finding) ---
# Scan a very narrow region around step 2 prediction (101.29)
# Capture the exact moment when wave changes from positive to negative

search_window = 0.5 # Search range (+- 0.5)
t_min = previous_prediction - search_window
t_max = previous_prediction + search_window

# Find point where chaos wave function becomes 0
try:
    final_chaos_prediction = brentq(chaos_wave_function, t_min, t_max)
    success = True
except ValueError:
    # Failure if no sign change in range (prediction range too far off)
    success = False
    final_chaos_prediction = previous_prediction

# --- 4. Final Result Analysis ---
print(f"Target (Actual):       {target_zero:.6f}")
print(f"2nd Step (Physics):    {previous_prediction:.6f} (Error: {abs(target_zero - previous_prediction):.6f})")

if success:
    print(f"3rd Step (Chaos):      {final_chaos_prediction:.6f}")
    
    final_error = abs(target_zero - final_chaos_prediction)
    print(f"-" * 40)
    print(f"Final Chaos Error:     {final_error:.6f}")
    
    if final_error < 0.001:
        print("\n🏆 RESULT: PERFECT SYNCHRONIZATION 🏆")
        print("Perfectly reverse-engineered the wave interference of primes.")
    else:
        print("\nResult: Still some quantum noise remains.")
else:
    print("Chaos prediction failed to converge in the window.")

# --- 5. Visualization (Appearance of Wave) ---
import matplotlib.pyplot as plt
t_vals = np.linspace(target_zero - 0.5, target_zero + 0.5, 100)
z_vals = [chaos_wave_function(t) for t in t_vals]

plt.figure(figsize=(10, 4))
plt.plot(t_vals, z_vals, label='Chaos Wave (Sum of Primes)', color='purple')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(target_zero, color='lime', linestyle='--', label='Actual Zero')
plt.scatter(final_chaos_prediction, 0, color='red', zorder=10, label='Predicted Zero')
plt.title('The Chaos Wave: Visualizing Prime Interference', fontsize=14)
plt.xlabel('Imaginary Part (t)', fontsize=12)
plt.ylabel('Z(t)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/figure8_chaos_wave.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 8 saved: data/figure8_chaos_wave.png")
