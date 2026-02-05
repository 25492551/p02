import numpy as np
from scipy.io.wavfile import write

# IPython.display is only used in Jupyter notebook environment (optional import)
try:
    import IPython.display as ipd
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False

def generate_zeta_bell(duration=5.0, sample_rate=44100):
    # 1. Riemann zeta zero data (first 50, imaginary part t values)
    # These values are the 'frequencies of the universe'
    zeros = np.array([
        14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
        52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448,
        79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6513, 95.8706, 98.8312, 101.3178,
        103.7255, 105.4466, 107.1686, 111.0295, 111.8747, 114.3202, 116.2266, 118.7907, 121.3701, 122.9468,
        124.2568, 127.5166, 129.5787, 131.0876, 133.4977, 134.7565, 138.1160, 139.7362, 141.1237, 143.1118
    ])

    # 2. Time axis generation
    t = np.linspace(0, duration, int(sample_rate * duration))

    # 3. Sound synthesis (Additive Synthesis)
    # Fundamental Frequency: Map first zero to 220Hz (near A3 note)
    # This makes 14.13 -> 220Hz and the rest follow proportionally
    base_freq = 220.0
    ratio = zeros / zeros[0]  # Ratio of zeros (non-commutative scale)
    
    waveform = np.zeros_like(t)
    
    # Convert each zero to an 'oscillator' and add them
    for i, r in enumerate(ratio):
        freq = base_freq * r
        
        # Amplitude decay (Envelope): Higher zeros have weaker energy and fade faster
        # This creates a 'bell-like' texture
        amplitude = 1.0 / (i + 1)**0.8 
        decay = np.exp(-t * (i * 0.1 + 0.5)) 
        
        # Sine wave synthesis
        waveform += amplitude * np.sin(2 * np.pi * freq * t) * decay

    # 4. Normalization (sound level adjustment)
    waveform = waveform / np.max(np.abs(waveform))
    
    return waveform, sample_rate

# --- Sound Generation Execution ---
sound_wave, sr = generate_zeta_bell(duration=8.0)

# Save to file (saved on server or local)
filename = "riemann_zeta_bell.wav"
write(filename, sr, (sound_wave * 32767).astype(np.int16))

print(f"🎵 '{filename}' file has been created.")
print("This sound is a 'non-commutative harmony' created by 50 zeros sounding simultaneously.")

# (If in Jupyter notebook environment, uncomment below to listen immediately)
# ipd.Audio(sound_wave, rate=sr)
