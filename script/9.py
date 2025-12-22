import numpy as np
from scipy.optimize import fsolve

# --- 1. 데이터 준비 ---
true_zeros = np.array([
    14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
    52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
    79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178
])

# 훈련 데이터 (29개) & 타겟 (30번째)
train_zeros = true_zeros[:-1]
target_zero = true_zeros[-1]
last_zero_actual = train_zeros[-1] # 29번째 실제값 (98.8312)

# --- 2. 개선된 거시 모델: 리만-폰 망골트 역함수 (Global Trend) ---
# N(T) 공식을 사용하여 n번째 영점의 "이상적인 위치"를 계산
def riemann_n_formula(t, n):
    # N(t) approx (t/2pi)log(t/2pi) - (t/2pi) + 7/8
    # n - 1 (인덱스 보정) 위치를 찾음
    val = (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - (t / (2 * np.pi)) + 0.875
    return val - n

# 29번째와 30번째의 "이론적 위치" 계산
# n=29, n=30에 해당하는 정확한 t값을 찾음 (로그 스퀴즈 반영)
theory_29 = fsolve(riemann_n_formula, x0=90, args=(29))[0]
theory_30 = fsolve(riemann_n_formula, x0=100, args=(30))[0]

print(f"Theory 29th: {theory_29:.4f}")
print(f"Theory 30th: {theory_30:.4f}")

# 이론적 간격 (Global Gap)
global_gap = theory_30 - theory_29
print(f"Global Log-Squeezed Gap: {global_gap:.4f}")


# --- 3. 미시적 보정: 스펙트럼 강성 (Spectral Rigidity) ---
# 29번째 영점이 이론적 위치보다 얼마나 벗어났는지 확인
# displacement > 0 이면 이론보다 밀려남(Pushed), < 0 이면 당겨짐(Pulled)
displacement_29 = last_zero_actual - theory_29
print(f"Displacement of 29th: {displacement_29:.4f} (Shift from theory)")

# [핵심 수정] 
# GUE 이론에 따르면 영점들의 편차는 로그함수적으로 천천히 변합니다.
# 29번이 밀려나 있었으면, 30번도 밀려나 있을 확률이 높습니다.
# 하지만 척력 때문에 그 정도는 약간 줄어들거나 유지됩니다.
# 보정 계수 (Stiffness Factor): 1.0에 가까울수록 강한 강성
stiffness = 0.95 

correction = displacement_29 * stiffness

# --- 4. 최종 예측 ---
# 예측값 = 30번 이론값 + 29번의 편차 보정
predicted_30 = theory_30 + correction

# --- 5. 결과 비교 ---
print("-" * 30)
print(f"Target (Actual):    {target_zero:.4f}")
print(f"Previous Prediction: 101.4500 (Error: +0.1322)")
print(f"New Prediction:      {predicted_30:.4f}")

error_new = abs(target_zero - predicted_30)
print(f"New Error:           {error_new:.4f}")

improvement = 0.1322 - error_new
print(f"Improvment:          {improvement:.4f}")

# --- 6. 시각화 ---
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
# 실제 영점들
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