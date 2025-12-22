import numpy as np
from scipy.optimize import brentq

# --- 1. 설정 ---
target_zero = 101.3178
previous_prediction = 101.2945 # 2단계에서 얻은 값 (대략)

# --- 2. 카오스 엔진: 리만-지겔 Z-함수 근사 (Z-function Approximation) ---
# 이것이 바로 '소수들의 간섭'을 계산하는 물리 엔진입니다.
# Z(t)가 0이 되는 곳이 곧 제타 함수의 영점입니다.

def riemann_siegel_theta(t):
    # 위상 보정 함수 (시스템의 거시적 회전)
    # theta(t) ~ (t/2) * log(t/2pi) - t/2 - pi/8
    return (t / 2.0) * np.log(t / (2.0 * np.pi)) - (t / 2.0) - (np.pi / 8.0)

def chaos_wave_function(t, n_cutoff=20):
    # 소수(와 정수)들의 파동 합성
    # Z(t) approx 2 * sum( cos(theta(t) - t*log(n)) / sqrt(n) )
    # n_cutoff: 얼마나 많은 '나비(소수)'의 날개짓을 고려할 것인가?
    # 이 항들이 서로 간섭하며 0.02의 오차를 메웁니다.
    
    theta = riemann_siegel_theta(t)
    val = 0.0
    
    # 1부터 N까지의 정수 파동 합산 (주요 소수들의 영향력 포함)
    for n in range(1, n_cutoff + 1):
        term = np.cos(theta - t * np.log(n)) / np.sqrt(n)
        val += term
        
    return 2.0 * val

# --- 3. 정밀 타격 (Root Finding) ---
# 2단계 예측값(101.29) 주변 아주 좁은 영역을 스캔합니다.
# 파동이 양수에서 음수로 바뀌는 정확한 순간을 포착합니다.

search_window = 0.5 # 검색 범위 (+- 0.5)
t_min = previous_prediction - search_window
t_max = previous_prediction + search_window

# 카오스 파동 함수에서 0이 되는 지점 찾기
try:
    final_chaos_prediction = brentq(chaos_wave_function, t_min, t_max)
    success = True
except ValueError:
    # 범위 내에 부호 변화가 없으면 실패 (예측 범위가 너무 빗나갔을 경우)
    success = False
    final_chaos_prediction = previous_prediction

# --- 4. 최종 결과 분석 ---
print(f"Target (Actual):       {target_zero:.6f}")
print(f"2nd Step (Physics):    {previous_prediction:.6f} (Error: {abs(target_zero - previous_prediction):.6f})")

if success:
    print(f"3rd Step (Chaos):      {final_chaos_prediction:.6f}")
    
    final_error = abs(target_zero - final_chaos_prediction)
    print(f"-" * 40)
    print(f"Final Chaos Error:     {final_error:.6f}")
    
    if final_error < 0.001:
        print("\n🏆 RESULT: PERFECT SYNCHRONIZATION 🏆")
        print("소수들의 파동 간섭을 완벽하게 역설계했습니다.")
    else:
        print("\nResult: Still some quantum noise remains.")
else:
    print("Chaos prediction failed to converge in the window.")

# --- 5. 시각화 (파동의 모습) ---
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