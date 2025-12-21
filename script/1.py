import numpy as np
import matplotlib.pyplot as plt

def simulated_zeta(t_values, sigma=0.5, noise_level=0.0, n_terms=1000):
    """
    리만 제타 함수의 근사값을 계산합니다.
    - t_values: 허수부 값들의 배열 (시간/파동의 진행)
    - sigma: 실수부 값 (보통 0.5)
    - noise_level: 님의 아이디어인 '비가환 소음(c, d)'의 세기
    - n_terms: 무한급수의 합을 계산할 항의 개수
    """
    zeta_vals = []
    
    for t in t_values:
        # 합계 초기화 (s = sigma + it)
        val = 0.0 + 0.0j
        
        for n in range(1, n_terms + 1):
            # 님의 가설 적용: 각 항마다 미세한 '비가환 소음'이 개입함
            # 이는 n번째 연산이 순수한 가환이 아님을 의미 (Random Jitter)
            random_phase = np.random.uniform(-1, 1) * noise_level
            
            # s에 소음 추가
            # 소음은 허수축(t)을 흔들거나, 실수축(sigma)을 흔들 수 있음
            # 여기서는 위상(Phase)을 흔드는 것으로 비가환성을 표현
            exponent = sigma + 1j * (t + random_phase)
            
            val += 1 / (n ** exponent)
            
        zeta_vals.append(abs(val)) # 크기(Magnitude) 저장
        
    return np.array(zeta_vals)

# --- 시뮬레이션 설정 ---
t_range = np.linspace(0, 50, 500) # t값 0부터 50까지 스캔

# 1. 리만의 세계 (소음 0) - 완벽한 간섭
zeta_ideal = simulated_zeta(t_range, sigma=0.5, noise_level=0.0)

# 2. 불확정 군의 세계 (소음 0.2) - 약간의 비가환성 개입
zeta_noisy_low = simulated_zeta(t_range, sigma=0.5, noise_level=0.2)

# 3. 완전한 혼돈 (소음 1.0) - 교환법칙 붕괴
zeta_noisy_high = simulated_zeta(t_range, sigma=0.5, noise_level=1.0)

# --- 시각화 ---
plt.figure(figsize=(12, 6))

# 리만의 세계 (파란색)
plt.plot(t_range, zeta_ideal, label='Riemann World (Order)', color='blue', alpha=0.8, linewidth=2)

# 불확정 세계 (주황색)
plt.plot(t_range, zeta_noisy_low, label='Uncertainty Group (Low Noise)', color='orange', alpha=0.7, linestyle='--')

# 혼돈 (초록색)
plt.plot(t_range, zeta_noisy_high, label='Chaos (High Noise)', color='green', alpha=0.4, linestyle=':')

# 기준선 (0)
plt.axhline(y=0, color='black', linewidth=1)

plt.title('Wave Interference: Order vs. Uncertainty', fontsize=15)
plt.xlabel('Imaginary Part (t)', fontsize=12)
plt.ylabel('|Zeta(s)|', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# 첫 번째 비자명 영점(t=14.13) 표시
plt.annotate('1st Zero (Order)', xy=(14.13, 0), xytext=(10, 3),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()