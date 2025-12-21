import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta

def energy_landscape(x_range, y_range, noise_sensitivity=2.0):
    """
    복소평면 상의 에너지 지형을 계산합니다.
    - x_range: 실수부 (Re(s)) 범위
    - y_range: 허수부 (Im(s)) 범위
    - noise_sensitivity: 임계선에서 멀어질수록 커지는 페널티 강도
    """
    X, Y = np.meshgrid(x_range, y_range)
    Z = X + 1j * Y
    
    # 1. 질서 에너지: 제타 함수의 크기 (낮을수록 안정)
    # log를 취해 영점 근처의 변화를 강조
    order_energy = np.log(np.abs(zeta(Z)) + 1e-9) 
    
    # 2. 혼돈 에너지 (Penalty): 임계선(0.5)에서 멀어질수록 비가환 소음 증가
    # 거리에 비례하여 에너지가 급격히 상승한다고 가정
    distance_from_critical = np.abs(X - 0.5)
    chaos_energy = noise_sensitivity * (distance_from_critical ** 2)
    
    # 총 에너지 H = Order + Chaos
    total_energy = order_energy + chaos_energy
    
    return X, Y, total_energy

# --- 시뮬레이션 설정 ---
# 실수부: 0 ~ 1 사이 (임계선 0.5 포함)
x = np.linspace(0, 1, 400)
# 허수부: 첫 번째 영점(14.13)부터 세 번째 영점(25.01) 근처까지
y = np.linspace(10, 30, 800)

X, Y, E = energy_landscape(x, y, noise_sensitivity=10.0)

# --- 시각화 (히트맵) ---
plt.figure(figsize=(10, 8))

# 에너지가 낮을수록(파란색/검은색) 안정적인 영점
# 에너지가 높을수록(노란색/붉은색) 불안정한 혼돈 상태
plt.contourf(X, Y, E, levels=50, cmap='RdYlBu_r') 
plt.colorbar(label='System Energy (Lower is More Stable)')

# 임계선 표시
plt.axvline(x=0.5, color='white', linestyle='--', alpha=0.5, label='Critical Line (Re=0.5)')

# 주요 영점 위치 표시 (이론값)
zeros = [14.134, 21.022, 25.011]
for z in zeros:
    plt.scatter(0.5, z, color='lime', s=100, marker='*', edgecolors='black', zorder=10, label='Zero' if z == zeros[0] else "")

plt.title('The Eye of the Storm: Stability of Zeros in Uncertainty Group', fontsize=14)
plt.xlabel('Real Part (Re(s))')
plt.ylabel('Imaginary Part (Im(s))')
plt.legend()
plt.show()