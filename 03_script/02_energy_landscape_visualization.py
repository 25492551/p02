import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta

def energy_landscape(x_range, y_range, noise_sensitivity=2.0):
    """
    Computes energy landscape on the complex plane.
    - x_range: Real part (Re(s)) range
    - y_range: Imaginary part (Im(s)) range
    - noise_sensitivity: Penalty intensity that increases away from critical line
    """
    X, Y = np.meshgrid(x_range, y_range)
    Z = X + 1j * Y
    
    # 1. Order Energy: Magnitude of zeta function (lower is more stable)
    # Take log to emphasize changes near zeros
    order_energy = np.log(np.abs(zeta(Z)) + 1e-9) 
    
    # 2. Chaos Energy (Penalty): Non-commutative noise increases away from critical line (0.5)
    # Assume energy rises rapidly proportional to distance
    distance_from_critical = np.abs(X - 0.5)
    chaos_energy = noise_sensitivity * (distance_from_critical ** 2)
    
    # Total Energy H = Order + Chaos
    total_energy = order_energy + chaos_energy
    
    return X, Y, total_energy

# --- Simulation Setup ---
# Real part: 0 ~ 1 (including critical line 0.5)
x = np.linspace(0, 1, 400)
# Imaginary part: Near first zero (14.13) to third zero (25.01)
y = np.linspace(10, 30, 800)

X, Y, E = energy_landscape(x, y, noise_sensitivity=10.0)

# --- Visualization (Heatmap) ---
plt.figure(figsize=(10, 8))

# Lower energy (blue/black) = stable zeros
# Higher energy (yellow/red) = unstable chaos state
plt.contourf(X, Y, E, levels=50, cmap='RdYlBu_r') 
plt.colorbar(label='System Energy (Lower is More Stable)')

# Mark critical line
plt.axvline(x=0.5, color='white', linestyle='--', alpha=0.5, label='Critical Line (Re=0.5)')

# Mark major zero locations (theoretical values)
zeros = [14.134, 21.022, 25.011]
for z in zeros:
    plt.scatter(0.5, z, color='lime', s=100, marker='*', edgecolors='black', zorder=10, label='Zero' if z == zeros[0] else "")

plt.title('The Eye of the Storm: Stability of Zeros in Uncertainty Group', fontsize=14)
plt.xlabel('Real Part (Re(s))')
plt.ylabel('Imaginary Part (Im(s))')
plt.legend()
plt.tight_layout()
plt.savefig('data/figure2_energy_landscape.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 2 saved: data/figure2_energy_landscape.png")
