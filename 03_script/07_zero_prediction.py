import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# --- 1. Data Preparation (Actual Riemann Zeta Zeros, Odlyzhko Table) ---
# First 30 zeros (imaginary part t values)
true_zeros = np.array([
    14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
    52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
    79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178
])

# Training data: first 29
train_zeros = true_zeros[:-1]
# Target data: 30th (value we need to predict)
target_zero = true_zeros[-1]

print(f"Target (Actual 30th Zero): {target_zero}")

# --- 2. Macroscopic Prediction ---
# Estimate approximate location of nth zero through inverse function of Riemann-von Mangoldt formula
# N(T) = n  =>  Solve for T

def riemann_n_formula(t, n):
    # N(t) = (t / 2pi) * log(t / 2pi) - (t / 2pi) + 7/8 (correction term)
    # Find t such that this value equals n
    val = (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - (t / (2 * np.pi)) + 0.875
    return val - n

# Calculate "average expected location" of 30th zero
macro_prediction = fsolve(riemann_n_formula, x0=100, args=(30))[0]
print(f"Macroscopic Prediction (Average): {macro_prediction:.4f}")

# --- 3. Microscopic Repulsion Correction ---
# Reflect 'repulsion' by analyzing spacing patterns with previous zeros

# Average of recent 5 gaps
recent_gaps = np.diff(train_zeros)[-5:]
avg_local_gap = np.mean(recent_gaps)

# Last zero (29th)
last_zero = train_zeros[-1]

# Apply Coulomb repulsion simulation logic:
# "If previous gap was narrower than average, this one will bounce out."
# "If previous gap was wider than average, this one will be pulled in."

# Previous gap (between 28th and 29th)
last_gap = train_zeros[-1] - train_zeros[-2]

# GUE (Gaussian Unitary Ensemble) property: gaps repel each other (Level Repulsion)
# Simple correction model: tendency to regress to mean (Elasticity)
elasticity = 0.6 # Restoring force coefficient (arbitrarily set)
correction = elasticity * (avg_local_gap - last_gap)

micro_prediction = last_zero + avg_local_gap + correction
print(f"Microscopic Prediction (Physics): {micro_prediction:.4f}")

# --- 4. Visualization ---
plt.figure(figsize=(10, 4))

# Actual 29 zeros
plt.scatter(train_zeros, np.zeros_like(train_zeros), color='black', marker='|', s=100, label='Past Zeros')

# Actual 30th zero (answer)
plt.scatter(target_zero, 0, color='lime', marker='*', s=300, zorder=10, label=f'Actual ({target_zero})')

# Macroscopic prediction (statistics)
plt.scatter(macro_prediction, 0, color='blue', marker='v', s=100, label=f'Macro Pred ({macro_prediction:.2f})')

# Microscopic prediction (physics)
plt.scatter(micro_prediction, 0, color='red', marker='^', s=100, label=f'Micro Pred ({micro_prediction:.2f})')

# Connection line
plt.annotate('', xy=(micro_prediction, 0.05), xytext=(last_zero, 0.05),
             arrowprops=dict(arrowstyle='->', color='red', alpha=0.5))

plt.title('Predicting the 30th Zero: Statistics vs. Physics', fontsize=14)
plt.xlabel('Imaginary Part (t)', fontsize=12)
plt.yticks([])
plt.xlim(90, 105)
plt.legend()
plt.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('data/figure6_zero_prediction.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 6 saved: data/figure6_zero_prediction.png")

# Error calculation
error_macro = abs(target_zero - macro_prediction)
error_micro = abs(target_zero - micro_prediction)

print(f"\n[Result Analysis]")
print(f"Macro Error: {error_macro:.4f}")
print(f"Micro Error: {error_micro:.4f}")
print(f"Winner: {'Micro (Physics Model)' if error_micro < error_macro else 'Macro (Statistics)'}")
