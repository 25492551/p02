import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# --- 1. 데이터 준비 (실제 리만 제타 영점, Odlyzhko Table) ---
# 처음 30개의 영점 (허수부 t값)
true_zeros = np.array([
    14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
    52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
    79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178
])

# 훈련 데이터: 처음 29개
train_zeros = true_zeros[:-1]
# 타겟 데이터: 30번째 (우리가 맞춰야 할 값)
target_zero = true_zeros[-1]

print(f"Target (Actual 30th Zero): {target_zero}")

# --- 2. 거시적 예측 (Macroscopic Prediction) ---
# 리만-폰 망골트 공식의 역함수를 통해 n번째 영점의 대략적 위치 추정
# N(T) = n  =>  Solve for T

def riemann_n_formula(t, n):
    # N(t) = (t / 2pi) * log(t / 2pi) - (t / 2pi) + 7/8 (보정항)
    # 이 값이 n이 되는 t를 찾음
    val = (t / (2 * np.pi)) * np.log(t / (2 * np.pi)) - (t / (2 * np.pi)) + 0.875
    return val - n

# 30번째 영점의 "평균적인 기대 위치" 계산
macro_prediction = fsolve(riemann_n_formula, x0=100, args=(30))[0]
print(f"Macroscopic Prediction (Average): {macro_prediction:.4f}")

# --- 3. 미시적 척력 보정 (Microscopic Repulsion) ---
# 이전 영점들과의 간격 패턴을 분석하여 '척력' 반영

# 최근 5개 간격의 평균
recent_gaps = np.diff(train_zeros)[-5:]
avg_local_gap = np.mean(recent_gaps)

# 마지막 영점 (29번째)
last_zero = train_zeros[-1]

# 쿨롱 척력 시뮬레이션 논리 적용:
# "이전 간격이 평균보다 좁았다면, 이번엔 튕겨 나갈 것이다."
# "이전 간격이 넓었다면, 이번엔 당겨질 것이다."

# 직전 간격 (28번째와 29번째 사이)
last_gap = train_zeros[-1] - train_zeros[-2]

# GUE(Gaussian Unitary Ensemble)의 성질: 간격은 서로 반발함 (Level Repulsion)
# 간단한 보정 모델: 평균으로 회귀하려는 성질 (Elasticity)
elasticity = 0.6 # 복원력 계수 (임의 설정)
correction = elasticity * (avg_local_gap - last_gap)

micro_prediction = last_zero + avg_local_gap + correction
print(f"Microscopic Prediction (Physics): {micro_prediction:.4f}")

# --- 4. 시각화 ---
plt.figure(figsize=(10, 4))

# 실제 29개 영점
plt.scatter(train_zeros, np.zeros_like(train_zeros), color='black', marker='|', s=100, label='Past Zeros')

# 실제 30번째 영점 (정답)
plt.scatter(target_zero, 0, color='lime', marker='*', s=300, zorder=10, label=f'Actual ({target_zero})')

# 거시적 예측 (통계)
plt.scatter(macro_prediction, 0, color='blue', marker='v', s=100, label=f'Macro Pred ({macro_prediction:.2f})')

# 미시적 예측 (물리)
plt.scatter(micro_prediction, 0, color='red', marker='^', s=100, label=f'Micro Pred ({micro_prediction:.2f})')

# 연결선
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

# 오차 계산
error_macro = abs(target_zero - macro_prediction)
error_micro = abs(target_zero - micro_prediction)

print(f"\n[Result Analysis]")
print(f"Macro Error: {error_macro:.4f}")
print(f"Micro Error: {error_micro:.4f}")
print(f"Winner: {'Micro (Physics Model)' if error_micro < error_macro else 'Macro (Statistics)'}")