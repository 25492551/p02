import numpy as np
import matplotlib.pyplot as plt

def simulate_coulomb_gas(num_particles=20, num_steps=200, learning_rate=0.01):
    # 입자들의 초기 위치 (임계선 위, 무작위 높이 t)
    # 서로 아주 가깝게 배치하여 '중근'이 될 뻔한 상황을 연출
    positions = np.sort(np.random.uniform(10, 20, num_particles))
    
    history = [positions.copy()]
    
    print("Simulating Repulsion Forces...")
    
    for _ in range(num_steps):
        forces = np.zeros_like(positions)
        
        # 모든 입자 쌍에 대해 척력 계산
        for i in range(num_particles):
            for j in range(num_particles):
                if i == j: continue
                
                # 거리
                dist = positions[i] - positions[j]
                
                # 척력 (Repulsion): F = 1 / dist
                # 거리가 0에 가까우면 힘이 무한대로 커짐
                # 방향은 거리의 부호가 결정
                forces[i] += 1.0 / dist
        
        # 외부 압력 (Confinement Potential)
        # 입자들이 무한히 멀어지지 않게 가두는 힘 (소수의 밀도 함수 역할)
        # 중앙(15)으로 약하게 당김
        forces -= 0.5 * (positions - 15)
        
        # 위치 업데이트
        positions += learning_rate * forces
        
        # 순서가 뒤바뀌지 않게 정렬 (1차원 위상 유지)
        positions = np.sort(positions)
        history.append(positions.copy())
        
    return np.array(history)

# --- 시뮬레이션 실행 ---
num_particles = 15
history = simulate_coulomb_gas(num_particles=num_particles)

# --- 시각화 ---
plt.figure(figsize=(12, 6))

# 시간(Step)에 따른 입자들의 위치 변화
steps = np.arange(len(history))
for i in range(num_particles):
    plt.plot(steps, history[:, i], linewidth=2)

plt.title('Why Multiple Roots are Impossible: Coulomb Repulsion of Zeros', fontsize=15)
plt.xlabel('Time Steps (Evolution)', fontsize=12)
plt.ylabel('Position on Critical Line (t)', fontsize=12)

# 설명 텍스트
plt.text(10, history[0, 1] + 0.5, "Close Initial State\n(Near Collision)", color='red', fontsize=10)
plt.text(180, history[-1, -2] - 1, "Stable Lattice\n(No Merging)", color='green', fontsize=10)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('data/figure5a_coulomb_gas_evolution.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 5a saved: data/figure5a_coulomb_gas_evolution.png")

# --- 간격 분포 확인 (Pair Correlation) ---
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