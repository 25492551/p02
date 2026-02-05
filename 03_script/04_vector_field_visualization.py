import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta

def get_vector_field(re_range, im_range):
    """
    Computes vector field (flow field) based on energy gradient.
    Zeros act as 'sinks' that draw in the flow.
    """
    re_vals = np.linspace(re_range[0], re_range[1], 40)
    im_vals = np.linspace(im_range[0], im_range[1], 80)
    
    U = np.zeros((len(im_vals), len(re_vals))) # Real axis velocity component
    V = np.zeros((len(im_vals), len(re_vals))) # Imaginary axis velocity component
    
    h = 1e-5
    
    for i, y in enumerate(im_vals):
        for j, x in enumerate(re_vals):
            s = x + 1j * y
            
            # Energy at current position
            # E = log(|zeta(s)|) + penalty
            # Flow direction is opposite to gradient
            
            # Numerical differentiation
            val_base = np.log(np.abs(zeta(s)) + 1e-9) + 5.0 * (abs(x - 0.5)**2)
            
            val_dx = np.log(np.abs(zeta(s + h)) + 1e-9) + 5.0 * (abs((x+h) - 0.5)**2)
            val_dy = np.log(np.abs(zeta(s + 1j*h)) + 1e-9) + 5.0 * (abs(x - 0.5)**2)
            
            grad_x = (val_dx - val_base) / h
            grad_y = (val_dy - val_base) / h
            
            # Flow is in energy decrease direction (-Gradient)
            U[i, j] = -grad_x
            V[i, j] = -grad_y
            
    return re_vals, im_vals, U, V

# --- Vector Field Calculation ---
# From first zero (14.13) to near third zero (25.01)
x_mesh, y_mesh, U, V = get_vector_field((0.1, 0.9), (12, 26))

# --- Visualization (Streamplot) ---
plt.figure(figsize=(10, 12))

# Draw streamlines: particle movement paths
# density: line density, color: speed (flow intensity)
speed = np.sqrt(U**2 + V**2)
plt.streamplot(x_mesh, y_mesh, U, V, color=speed, cmap='autumn', density=1.5, linewidth=1)

# Critical line
plt.axvline(x=0.5, color='black', linestyle='--', alpha=0.5)

# Mark zero locations
zeros = [14.135, 21.022, 25.011]
labels = ["1st Zero", "2nd Zero", "3rd Zero"]

for z, lbl in zip(zeros, labels):
    plt.scatter(0.5, z, color='blue', s=100, zorder=10, edgecolors='white')
    plt.text(0.55, z, lbl, fontsize=12, verticalalignment='center')

plt.title('Hidden Rules: Vorticity & Basin Size', fontsize=16)
plt.xlabel('Real Part (Re)', fontsize=12)
plt.ylabel('Imaginary Part (Im)', fontsize=12)
plt.xlim(0.1, 0.9)
plt.ylim(12, 26)

plt.tight_layout()
plt.savefig('data/figure4_vector_field.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 4 saved: data/figure4_vector_field.png")
