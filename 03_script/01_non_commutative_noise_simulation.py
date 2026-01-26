import numpy as np
import matplotlib.pyplot as plt

def simulated_zeta(t_values, sigma=0.5, noise_level=0.0, n_terms=1000):
    """
    Computes approximate values of the Riemann zeta function.
    - t_values: Array of imaginary part values (time/wave progression)
    - sigma: Real part value (usually 0.5)
    - noise_level: Intensity of 'non-commutative noise (c, d)' idea
    - n_terms: Number of terms to compute the infinite series sum
    """
    zeta_vals = []
    
    for t in t_values:
        # Initialize sum (s = sigma + it)
        val = 0.0 + 0.0j
        
        for n in range(1, n_terms + 1):
            # Apply hypothesis: subtle 'non-commutative noise' intervenes at each term
            # This means the nth operation is not purely commutative (Random Jitter)
            random_phase = np.random.uniform(-1, 1) * noise_level
            
            # Add noise to s
            # Noise can shake the imaginary axis (t) or real axis (sigma)
            # Here, non-commutativity is expressed by shaking the phase
            exponent = sigma + 1j * (t + random_phase)
            
            val += 1 / (n ** exponent)
            
        zeta_vals.append(abs(val)) # Store magnitude
        
    return np.array(zeta_vals)

# --- Simulation Setup ---
t_range = np.linspace(0, 50, 500) # Scan t values from 0 to 50

# 1. Riemann's World (noise 0) - Perfect interference
zeta_ideal = simulated_zeta(t_range, sigma=0.5, noise_level=0.0)

# 2. Uncertainty Group's World (noise 0.2) - Slight non-commutativity intervention
zeta_noisy_low = simulated_zeta(t_range, sigma=0.5, noise_level=0.2)

# 3. Complete Chaos (noise 1.0) - Commutative law collapse
zeta_noisy_high = simulated_zeta(t_range, sigma=0.5, noise_level=1.0)

# --- Visualization ---
plt.figure(figsize=(12, 6))

# Riemann's World (blue)
plt.plot(t_range, zeta_ideal, label='Riemann World (Order)', color='blue', alpha=0.8, linewidth=2)

# Uncertainty World (orange)
plt.plot(t_range, zeta_noisy_low, label='Uncertainty Group (Low Noise)', color='orange', alpha=0.7, linestyle='--')

# Chaos (green)
plt.plot(t_range, zeta_noisy_high, label='Chaos (High Noise)', color='green', alpha=0.4, linestyle=':')

# Baseline (0)
plt.axhline(y=0, color='black', linewidth=1)

plt.title('Wave Interference: Order vs. Uncertainty', fontsize=15)
plt.xlabel('Imaginary Part (t)', fontsize=12)
plt.ylabel('|Zeta(s)|', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# Mark first non-trivial zero (t=14.13)
plt.annotate('1st Zero (Order)', xy=(14.13, 0), xytext=(10, 3),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.tight_layout()
plt.savefig('data/figure1_non_commutative_noise.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 1 saved: data/figure1_non_commutative_noise.png")
