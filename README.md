# P02 Project: Riemann Zeta Function Visualization and Simulation

## Project Overview

The P02 project performs visualization and simulation of non-trivial zeros of the Riemann Zeta Function.

Based on the prime distribution analysis and Riemann hypothesis research covered in the P01 project, this project explores the mathematical properties and physical interpretations of the zeros of the Riemann zeta function.

## Project Structure

```
P02/
├── data/              # Data files
├── log/               # Log files
│   ├── chat log/      # Chat logs
│   └── job log/       # Job logs
├── plan/              # Planning documents
├── report/            # Analysis reports
├── script/            # Python scripts
│   ├── 1.py          # Riemann zeta function simulation (non-commutative noise)
│   ├── 2.py          # Energy landscape visualization
│   ├── 3.py          # Particle simulation
│   ├── 4.py          # Vector field visualization
│   ├── 5.py          # Coulomb gas simulation
│   ├── 7.py          # Zero prediction (Step 1: Macroscopic prediction)
│   ├── 8.py          # Zeta bell sound generation
│   ├── 9.py          # Spectral rigidity prediction (Step 2: Microscopic correction)
│   └── 10.py         # Chaos wave prediction (Step 3: Refinement)
└── README.md          # This file

```

## Main Script Descriptions

### 1.py - Riemann Zeta Function Simulation
Approximation and visualization of the Riemann zeta function with non-commutative noise applied. Comparative analysis of Riemann's world (order) and the world of indefinite groups (chaos).

### 2.py - Energy Landscape Visualization
Analysis of zero stability by calculating the energy landscape on the complex plane. System energy is computed as the sum of order energy and chaos energy.

### 3.py - Particle Simulation
Simulation of the evolution process of particles moving along the gradient of the energy function. Visualization of particle trajectories converging near zeros.

### 4.py - Vector Field Visualization
Visualization of flow where zeros act as 'sinks' by calculating vector fields (flow fields) based on energy gradients.

### 5.py - Coulomb Gas Simulation
Physical explanation of why multiple roots are impossible by simulating repulsion between zeros.

### 7.py - Zero Prediction (Step 1: Macroscopic Prediction)
A model that predicts the location of the next zero by combining macroscopic prediction using the Riemann-von Mangoldt formula and microscopic prediction using Coulomb repulsion.

### 8.py - Zeta Bell Sound Generation
Synthesis of sound by converting zeros of the Riemann zeta function into frequencies. Generates non-commutative harmonies.

### 9.py - Spectral Rigidity Prediction (Step 2: Microscopic Correction)
Improvement of zero prediction by applying the concept of Spectral Rigidity from GUE theory. A microscopic correction model that reflects the correlation of deviations between adjacent zeros.

### 10.py - Chaos Wave Prediction (Step 3: Refinement)
Precise calculation of zero locations using a chaos engine based on Riemann-Siegel Z-function approximation. Final refinement step through wave interference of primes.

## 3-Step Zero Prediction Process

Zero prediction follows a three-step refinement process:

1. **Step 1 (script/7.py) - Macroscopic Prediction**: Calculation of theoretical location using the Riemann-von Mangoldt formula
2. **Step 2 (script/9.py) - Microscopic Correction**: Deviation correction using spectral rigidity
3. **Step 3 (script/10.py) - Chaos Engine**: Precise calculation using Riemann-Siegel Z-function approximation

Accuracy improves at each step, enabling precise prediction with error less than 0.001 in the final stage.

## Dependencies

Main Python packages:
- numpy
- matplotlib
- scipy

For details, please refer to `requirements.txt`.

## Usage

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run scripts:
```bash
python script/1.py
```

## Related Projects

- **P01**: Prime distribution analysis and Riemann hypothesis research

## References

- Riemann, B. (1859): "Über die Anzahl der Primzahlen unter einer gegebenen Größe"
- Edwards, H. M. (2001): "Riemann's Zeta Function"
- Davenport, H. (2000): "Multiplicative Number Theory"
- von Mangoldt, H. (1905): Riemann-von Mangoldt formula
- Siegel, C. L. (1932): Riemann-Siegel formula
- GUE Theory: Gaussian Unitary Ensemble and random matrix theory

## License

This project is created for research and educational purposes.
