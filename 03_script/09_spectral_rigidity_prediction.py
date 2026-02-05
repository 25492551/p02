import numpy as np
from scipy.optimize import fsolve

# --- 1. Data Preparation ---
true_zeros = np.array([
    14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
    52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
    79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178
])

# Training data (29) & target (30th)
train_zeros = true_zeros[:-1]
target_zero = true_zeros[-1]
last_zero_actual = train_zeros[-1] # 29th actual value (98.8312)

# --- 2. Improved Macroscopic Model: Riemann-von Mangoldt Inverse Function (Global Trend) ---
# Calculate "ideal location" of nth zero using N(T) formula
def riemann_n_formula(t, n):
    # N(t) approx (t/2pi)log(t/2pi) - (t/2pi) + 7/8
    # Find location for n - 1 (index correction)
    val = (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - (t / (2 * np.pi)) + 0.875
    return val - n

# Calculate "theoretical location" of 29th and 30th
# Find exact t values corresponding to n=29, n=30 (reflecting log squeeze)
theory_29 = fsolve(riemann_n_formula, x0=90, args=(29))[0]
theory_30 = fsolve(riemann_n_formula, x0=100, args=(30))[0]

print(f"Theory 29th: {theory_29:.4f}")
print(f"Theory 30th: {theory_30:.4f}")

# Theoretical gap (Global Gap)
global_gap = theory_30 - theory_29
print(f"Global Log-Squeezed Gap: {global_gap:.4f}")


# --- 3. Microscopic Correction: Spectral Rigidity ---
# Check how much the 29th zero deviates from theoretical location
# displacement > 0 means pushed from theory, < 0 means pulled toward theory
displacement_29 = last_zero_actual - theory_29
print(f"Displacement of 29th: {displacement_29:.4f} (Shift from theory)")

# [Key Modification] 
# According to GUE theory, deviations of zeros change logarithmically slowly.
# If 29th was pushed out, 30th is likely to be pushed out as well.
# However, due to repulsion, the degree is slightly reduced or maintained.
# Correction coefficient (Stiffness Factor): Closer to 1.0 means stronger stiffness
stiffness = 0.95 

correction = displacement_29 * stiffness

# --- 4. Final Prediction ---
# Prediction = 30th theoretical value + 29th deviation correction
predicted_30 = theory_30 + correction

# --- 5. Result Comparison ---
print("-" * 30)
print(f"Target (Actual):    {target_zero:.4f}")
print(f"Previous Prediction: 101.4500 (Error: +0.1322)")
print(f"New Prediction:      {predicted_30:.4f}")

error_new = abs(target_zero - predicted_30)
print(f"New Error:           {error_new:.4f}")

improvement = 0.1322 - error_new
print(f"Improvment:          {improvement:.4f}")

# --- 6. Visualization ---
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
# Actual zeros
plt.scatter(train_zeros, np.zeros_like(train_zeros), color='black', marker='|', s=100, label='Past Zeros')
plt.scatter(target_zero, 0, color='lime', marker='*', s=300, zorder=10, label=f'Actual 30th ({target_zero:.4f})')
plt.scatter(theory_30, 0, color='blue', marker='v', s=100, label=f'Theoretical ({theory_30:.4f})')
plt.scatter(predicted_30, 0, color='red', marker='^', s=100, label=f'Predicted ({predicted_30:.4f})')

plt.title('Spectral Rigidity Prediction: 30th Zero', fontsize=14)
plt.xlabel('Imaginary Part (t)', fontsize=12)
plt.ylabel('', fontsize=12)
plt.yticks([])
plt.xlim(95, 103)
plt.legend()
plt.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('data/figure7_spectral_rigidity.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 7 saved: data/figure7_spectral_rigidity.png")
