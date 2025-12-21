import numpy as np
import matplotlib.pyplot as plt

def zeta_approx_vectorized(s, n_terms=1000):
    """
    Computes Riemann Zeta function using Dirichlet eta function for a an array of complex numbers s.
    Valid for Re(s) > 0.
    s: numpy array of complex numbers shape (M,)
    """
    # Create n array: shape (1, n_terms)
    n = np.arange(1, n_terms + 1).reshape(1, -1)
    
    # Reshape s for broadcasting: shape (M, 1)
    s_reshaped = s.reshape(-1, 1)
    
    # Calculate terms: (-1)^(n-1) / n^s
    # alternating signs: 1, -1, 1, -1 ...
    signs = np.power(-1.0, np.arange(0, n_terms)).reshape(1, -1)
    
    # Denominators: n^s
    denoms = np.power(n, s_reshaped)
    
    # Eta function sum
    eta = np.sum(signs / denoms, axis=1)
    
    # Convert to Zeta: Zeta(s) = Eta(s) / (1 - 2^(1-s))
    factor = 1.0 - np.power(2.0, 1.0 - s)
    
    return eta / factor

def energy_function(s, noise_sensitivity=5.0):
    # Order Energy: log(|zeta(s)|)
    # Chaos Energy: penalty based on distance from Re(s)=0.5
    
    z_val = zeta_approx_vectorized(s)
    # Add epsilon to avoid log(0)
    order_E = np.log(np.abs(z_val) + 1e-9)
    
    # Chaos Energy
    dist = np.abs(s.real - 0.5)
    chaos_E = noise_sensitivity * (dist ** 2)
    
    return order_E + chaos_E

def get_gradient(s, h=1e-5):
    # Numerical gradient calculation
    # Gradient with respect to Real and Imaginary parts separately
    
    # Perturb real part
    E_plus_r = energy_function(s + h)
    E_minus_r = energy_function(s - h)
    grad_r = (E_plus_r - E_minus_r) / (2 * h)
    
    # Perturb imaginary part
    E_plus_i = energy_function(s + 1j*h)
    E_minus_i = energy_function(s - 1j*h)
    grad_i = (E_plus_i - E_minus_i) / (2 * h)
    
    return grad_r + 1j * grad_i

# --- Simulation Parameters ---
np.random.seed(42)
num_particles = 300
num_steps = 60
learning_rate = 0.05
noise_level = 0.02 # Stochastic noise (simulating quantum jitter)

# Initialize particles randomly
# Real part: 0.2 to 0.8
# Imaginary part: 10 to 30 (covering first few zeros)
initial_real = np.random.uniform(0.1, 0.9, num_particles)
initial_imag = np.random.uniform(10, 30, num_particles)
particles = initial_real + 1j * initial_imag

# Track history for visualization
history = [particles.copy()]

# --- Main Loop ---
print("Starting Particle Simulation...")
for step in range(num_steps):
    # Calculate gradients
    grads = get_gradient(particles)
    
    # Update positions: Move opposite to gradient (Downhill)
    # Add stochastic noise (Brownian motion / Quantum fluctuation)
    stochastic_kick = (np.random.randn(num_particles) + 1j * np.random.randn(num_particles)) * noise_level
    
    particles = particles - learning_rate * grads + stochastic_kick
    
    # Boundary conditions (Keep within reasonable bounds to prevent divergence)
    # Clamp Real part to (0, 1) just to keep simulation focused
    particles.real = np.clip(particles.real, 0.01, 0.99)
    
    history.append(particles.copy())

print("Simulation Complete.")

# --- Visualization ---
plt.figure(figsize=(12, 8))

# Plot initial positions
plt.scatter(history[0].real, history[0].imag, color='gray', alpha=0.3, s=10, label='Initial Position (Chaos)')

# Plot trajectories for a subset of particles to reduce clutter
for i in range(0, num_particles, 5): # Plot every 5th particle
    traj = np.array([h[i] for h in history])
    plt.plot(traj.real, traj.imag, color='blue', alpha=0.1, linewidth=0.5)

# Plot final positions
final_particles = history[-1]
plt.scatter(final_particles.real, final_particles.imag, color='red', alpha=0.8, s=20, label='Final Position (Order)')

# Plot Critical Line
plt.axvline(x=0.5, color='black', linestyle='--', linewidth=1.5, label='Critical Line (Re=0.5)')

# Mark known zeros
known_zeros = [14.135, 21.022, 25.011]
for z in known_zeros:
    plt.scatter(0.5, z, color='lime', s=100, marker='*', edgecolors='black', zorder=10, label='True Zero' if z == known_zeros[0] else "")

plt.title(f'Evolution of {num_particles} Particles in "Uncertainty Group" Field', fontsize=16)
plt.xlabel('Real Part (Re)', fontsize=12)
plt.ylabel('Imaginary Part (Im)', fontsize=12)
plt.legend(loc='upper right')
plt.xlim(0, 1)
plt.ylim(10, 30)
plt.grid(True, alpha=0.3)

plt.savefig('particle_simulation.png')