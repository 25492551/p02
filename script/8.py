import numpy as np
from scipy.io.wavfile import write

# IPython.display는 주피터 노트북 환경에서만 사용 (선택적 import)
try:
    import IPython.display as ipd
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False

def generate_zeta_bell(duration=5.0, sample_rate=44100):
    # 1. 리만 제타 영점 데이터 (처음 50개, 허수부 t값)
    # 이 값들이 바로 '우주의 주파수'입니다.
    zeros = np.array([
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
        52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
        79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178,
        103.7255, 105.4466, 107.1686, 111.0295, 111.8747, 114.3202, 116.2266, 118.7907, 121.3701, 122.9468,
        124.2568, 127.5166, 129.5787, 131.0876, 133.4977, 134.7565, 138.1160, 139.7362, 141.1237, 143.1118
    ])

    # 2. 시간축 생성
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 3. 소리 합성 (Additive Synthesis)
    # 기본 주파수(Fundamental Frequency): 첫 번째 영점을 220Hz(A3음 근처)로 매핑
    # 이렇게 하면 14.13 -> 220Hz가 되고 나머지는 비율대로 따라갑니다.
    base_freq = 220.0
    ratio = zeros / zeros[0]  # 영점들의 비율 (비가환적 음계)
    
    waveform = np.zeros_like(t)
    
    # 각 영점을 '진동자(Oscillator)'로 변환하여 더함
    for i, r in enumerate(ratio):
        freq = base_freq * r
        
        # 진폭 감쇠 (Envelope): 높은 영점일수록 에너지가 약하고 빨리 사라짐
        # 이것이 '종소리' 같은 질감을 만듭니다.
        amplitude = 1.0 / (i + 1)**0.8 
        decay = np.exp(-t * (i * 0.1 + 0.5)) 
        
        # 사인파 합성
        waveform += amplitude * np.sin(2 * np.pi * freq * t) * decay

    # 4. 정규화 (소리 크기 조절)
    waveform = waveform / np.max(np.abs(waveform))
    
    return waveform, sample_rate

# --- 소리 생성 실행 ---
sound_wave, sr = generate_zeta_bell(duration=8.0)

# 파일로 저장 (서버나 로컬에 저장됨)
filename = "riemann_zeta_bell.wav"
write(filename, sr, (sound_wave * 32767).astype(np.int16))

print(f"🎵 '{filename}' 파일이 생성되었습니다.")
print("이 소리는 영점 50개가 동시에 울리며 만드는 '비가환적 화음'입니다.")

# (주피터 노트북 환경이라면 아래 주석을 해제하여 바로 들을 수 있습니다)
# ipd.Audio(sound_wave, rate=sr)