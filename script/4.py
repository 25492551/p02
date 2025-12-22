import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta

def get_vector_field(re_range, im_range):
    """
    에너지 기울기에 따른 벡터장(유동장)을 계산합니다.
    영점이 '싱크(Sink)'로 작용하여 흐름을 빨아들입니다.
    """
    re_vals = np.linspace(re_range[0], re_range[1], 40)
    im_vals = np.linspace(im_range[0], im_range[1], 80)
    
    U = np.zeros((len(im_vals), len(re_vals))) # 실수축 속도 성분
    V = np.zeros((len(im_vals), len(re_vals))) # 허수축 속도 성분
    
    h = 1e-5
    
    for i, y in enumerate(im_vals):
        for j, x in enumerate(re_vals):
            s = x + 1j * y
            
            # 현재 위치의 에너지
            # E = log(|zeta(s)|) + penalty
            # 미분(Gradient)의 반대 방향이 흐름의 방향
            
            # 수치 미분
            val_base = np.log(np.abs(zeta(s)) + 1e-9) + 5.0 * (abs(x - 0.5)**2)
            
            val_dx = np.log(np.abs(zeta(s + h)) + 1e-9) + 5.0 * (abs((x+h) - 0.5)**2)
            val_dy = np.log(np.abs(zeta(s + 1j*h)) + 1e-9) + 5.0 * (abs(x - 0.5)**2)
            
            grad_x = (val_dx - val_base) / h
            grad_y = (val_dy - val_base) / h
            
            # 흐름은 에너지 감소 방향 (-Gradient)
            U[i, j] = -grad_x
            V[i, j] = -grad_y
            
    return re_vals, im_vals, U, V

# --- 벡터장 계산 ---
# 첫 번째 영점(14.13)부터 세 번째 영점(25.01) 부근까지
x_mesh, y_mesh, U, V = get_vector_field((0.1, 0.9), (12, 26))

# --- 시각화 (Streamplot) ---
plt.figure(figsize=(10, 12))

# 유선(Streamline) 그리기: 입자의 이동 경로
# density: 선의 밀도, color: 속도(흐름의 세기)
speed = np.sqrt(U**2 + V**2)
plt.streamplot(x_mesh, y_mesh, U, V, color=speed, cmap='autumn', density=1.5, linewidth=1)

# 임계선
plt.axvline(x=0.5, color='black', linestyle='--', alpha=0.5)

# 영점 위치 표시
zeros = [14.135, 21.022, 25.011]
labels = ["1st Zero", "2nd Zero", "3rd Zero"]

for z, lbl in zip(zeros, labels):
    plt.scatter(0.5, z, color='blue', s=100, zorder=10, edgecolors='white')
    plt.text(0.55, z, lbl, fontsize=12, verticalalignment='center')

plt.title('Hidden Rules: Vorticity & Basin Size', fontsize=16)
plt.xlabel('Real Part (Re)', fontsize=12)
plt.ylabel('Imaginary Part (Im)', fontsize=12)
plt.xlim(0.1, 0.9)
plt.ylim(12, 26)

plt.tight_layout()
plt.savefig('data/figure4_vector_field.png', dpi=300, bbox_inches='tight')
plt.close()
print("Figure 4 saved: data/figure4_vector_field.png")