import numpy as np
import matplotlib.pyplot as plt

def simulate_coulomb_gas(num_particles=20, num_steps=200, learning_rate=0.01):
    # Initial positions of particles (on critical line, random height t)
    # Placed very close together to create a situation near 'multiple roots'
    positions = np.sort(np.random.uniform(10, 20, num_particles))
    
    history = [positions.copy()]
    
    print("Simulating Repulsion Forces...")
    
    for _ in range(num_steps):
        forces = np.zeros_like(positions)
        
        # Calculate repulsion for all particle pairs
        for i in range(num_particles):
            for j in range(num_particles):
                if i == j: continue
                
                # Distance
                dist = positions[i] - positions[j]
                
                # Repulsion: F = 1 / dist
                # Force becomes infinite as distance approaches 0
                # Direction determined by sign of distance
                forces[i] += 1.0 / dist
        
        # External pressure (Confinement Potential)
        # Force that confines particles so they don't move infinitely far (acts as prime density function)
        # Weak pull toward center (15)
        forces -= 0.5 * (positions - 15)
        
        # Update positions
        positions += learning_rate * forces
        
        # Sort to maintain order (maintain 1D topology)
        positions = np.sort(positions)
        history.append(positions.copy())
        
    return np.array(history)

# --- Simulation Execution ---
num_particles = 15
history = simulate_coulomb_gas(num_particles=num_particles)

# --- Visualization ---
plt.figure(figsize=(12, 6))

# Position changes of particles over time (Steps)
steps = np.arange(len(history))
for i in range(num_particles):
    plt.plot(steps, history[:, i], linewidth=2)

plt.title('Why Multiple Roots are Impossible: Coulomb Repulsion of Zeros', fontsize=15)
plt.xlabel('Time Steps (Evolution)', fontsize=12)
plt.ylabel('Position on Critical Line (t)', fontsize=12)

# Descriptive text
plt.text(10, history[0, 1] + 0.5, "Close Initial State\n(Near Collision)", color='red', fontsize=10)
plt.text(180, history[-1, -2] - 1, "Stable Lattice\n(No Merging)", color='green', fontsize=10)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/figure5a_coulomb_gas_evolution.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 5a saved: data/figure5a_coulomb_gas_evolution.png")

# --- Spacing Distribution Check (Pair Correlation) ---
final_positions = history[-1]
spacings = np.diff(final_positions)

plt.figure(figsize=(8, 4))
plt.hist(spacings, bins=10, color='purple', alpha=0.7, rwidth=0.9)
plt.title('Spacing Distribution between Zeros', fontsize=12)
plt.xlabel('Distance to Next Zero', fontsize=10)
plt.ylabel('Frequency', fontsize=10)
plt.axvline(x=0, color='red', linestyle='--', label='Distance 0 (Multiple Root)')
plt.legend()
plt.tight_layout()
plt.savefig('data/figure5b_coulomb_gas_spacing.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 5b saved: data/figure5b_coulomb_gas_spacing.png")
