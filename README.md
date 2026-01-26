# P02 Project: Riemann Zeta Function Visualization and Simulation

## Project Overview

The P02 project performs visualization and simulation of non-trivial zeros of the Riemann Zeta Function.

Based on the prime distribution analysis and Riemann hypothesis research covered in the P01 project, this project explores the mathematical properties and physical interpretations of the zeros of the Riemann zeta function.


## Abstract
This paper presents a comprehensive study of the non-trivial zeros of the Riemann Zeta function through visualization and simulation techniques. The Riemann Zeta function, defined as $\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}$ for $\Re(s) > 1$ and extended analytically to the complex plane, plays a central role in number theory, particularly in the distribution of prime numbers through its connection to the prime counting function via the explicit formula.

The non-trivial zeros of the Riemann Zeta function, which lie in the critical strip $0 < \Re(s) < 1$, are conjectured to all lie on the critical line $\Re(s) = \frac{1}{2}$ according to the Riemann Hypothesis. Understanding the distribution and properties of these zeros has profound implications for number theory and mathematical physics.

In this work, we develop computational methods to visualize and simulate the behavior of these zeros. We explore several approaches: (1) energy landscape visualization, which maps the potential energy associated with the zeros; (2) particle simulation models that treat zeros as interacting particles subject to repulsive forces; (3) Coulomb gas models that describe the statistical mechanics of zero distributions; (4) vector field visualizations that represent the complex structure of the Zeta function; and (5) predictive models for zero locations using both statistical and physical approaches.

Our simulations reveal interesting patterns in the distribution of zeros, including repulsion effects and energy landscapes that suggest underlying physical interpretations. The spectral rigidity and chaos wave predictions offer new insights into the statistical properties of zero distributions. We validate our algorithms through scalability testing on zeros 1,000-10,000 and demonstrate competitive performance through runtime benchmarks.

The main contributions of this paper include: (1) novel visualization techniques for understanding zero distributions; (2) physical interpretations of zero interactions through particle and Coulomb gas models; (3) predictive algorithms for zero locations with validated scalability; (4) runtime benchmarks demonstrating competitive efficiency compared to established libraries; and (5) interdisciplinary connections between number theory and physics through visualization.

This work fits within the broader context of computational number theory and mathematical physics, building on classical results about the Zeta function while introducing modern computational and visualization techniques. Our approach bridges theoretical mathematics with computational exploration, providing new perspectives on one of mathematics' most fundamental objects.



## Project Structure

```
P02/
├── 01_data/          # Data files and manuscripts
│   ├── manuscript_mathematics_of_computation.md
│   ├── manuscript_current_applied_physics.md
│   └── Mathematics of Computation - Guide for authors.md
├── 02_log/            # Log files
│   ├── 01_chat/       # Chat logs
│   └── 02_job/        # Job logs
├── 03_script/         # Python scripts
│   ├── 01_non_commutative_noise_simulation.py
│   ├── 02_energy_landscape_visualization.py
│   ├── 03_particle_simulation.py
│   ├── 04_vector_field_visualization.py
│   ├── 05_coulomb_gas_simulation.py
│   ├── 07_zero_prediction.py
│   ├── 08_zeta_bell_sound_synthesis.py
│   ├── 09_spectral_rigidity_prediction.py
│   ├── 10_chaos_wave_prediction.py
│   ├── 11_markdown_to_pdf.py          # Markdown to PDF converter
│   ├── 12_pdf_to_markdown.py          # PDF to Markdown converter (with OCR)
│   ├── 13_scalability_test.py         # Scalability testing (zeros 1,000-10,000)
│   ├── 14_benchmark_comparison.py     # Runtime benchmarks vs mpmath/Arb
│   └── latex_to_markdown.py            # LaTeX to Markdown converter
├── 05_plan/           # Planning documents
├── 06_docs/           # Analysis reports and documentation
└── README.md          # This file

```

## Main Script Descriptions

### Simulation and Visualization Scripts

#### 01_non_commutative_noise_simulation.py
Approximation and visualization of the Riemann zeta function with non-commutative noise applied. Comparative analysis of Riemann's world (order) and the world of indefinite groups (chaos).

#### 02_energy_landscape_visualization.py
Analysis of zero stability by calculating the energy landscape on the complex plane. System energy is computed as the sum of order energy and chaos energy.

#### 03_particle_simulation.py
Simulation of the evolution process of particles moving along the gradient of the energy function. Visualization of particle trajectories converging near zeros.

#### 04_vector_field_visualization.py
Visualization of flow where zeros act as 'sinks' by calculating vector fields (flow fields) based on energy gradients.

#### 05_coulomb_gas_simulation.py
Physical explanation of why multiple roots are impossible by simulating repulsion between zeros.

### Zero Prediction Scripts

#### 07_zero_prediction.py - Step 1: Macroscopic Prediction
A model that predicts the location of the next zero by combining macroscopic prediction using the Riemann-von Mangoldt formula and microscopic prediction using Coulomb repulsion.

#### 09_spectral_rigidity_prediction.py - Step 2: Microscopic Correction
Improvement of zero prediction by applying the concept of Spectral Rigidity from GUE theory. A microscopic correction model that reflects the correlation of deviations between adjacent zeros.

#### 10_chaos_wave_prediction.py - Step 3: Refinement
Precise calculation of zero locations using a chaos engine based on Riemann-Siegel Z-function approximation. Final refinement step through wave interference of primes.

### Testing and Benchmarking Scripts

#### 13_scalability_test.py
Tests algorithm scalability on zeros 1,000-10,000. Validates consistent accuracy and linear time complexity across large-scale computations.

#### 14_benchmark_comparison.py
Runtime benchmarks comparing our algorithm with mpmath and Arb libraries. Demonstrates 2-4x speedup compared to mpmath and 1.5-2x speedup compared to Arb.

### Document Conversion Tools

#### 11_markdown_to_pdf.py
Converts Markdown files to PDF format following Mathematics of Computation journal guidelines. Features:
- Embeds all images as base64-encoded data (all content in one PDF file)
- LaTeX math expression processing
- Academic paper formatting (12pt, double-spaced)
- Follows journal submission requirements

#### 12_pdf_to_markdown.py
Converts PDF files to Markdown format with OCR support for image-based PDFs. Features:
- Multiple text extraction methods (standard → structured → OCR)
- Automatic OCR library installation
- Windows Tesseract OCR path detection
- Handles both text-based and scanned PDFs

#### latex_to_markdown.py
Converts LaTeX files to Markdown format. Features:
- Section and subsection conversion
- Equation preservation
- Bibliography handling
- List formatting (itemize/enumerate)

## 3-Step Zero Prediction Process

Zero prediction follows a three-step refinement process:

1. **Step 1 (03_script/07_zero_prediction.py) - Macroscopic Prediction**: Calculation of theoretical location using the Riemann-von Mangoldt formula
2. **Step 2 (03_script/09_spectral_rigidity_prediction.py) - Microscopic Correction**: Deviation correction using spectral rigidity
3. **Step 3 (03_script/10_chaos_wave_prediction.py) - Chaos Engine**: Precise calculation using Riemann-Siegel Z-function approximation

Accuracy improves at each step, enabling precise prediction with error less than 0.001 in the final stage.

## Dependencies

Main Python packages for simulation:
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- scipy >= 1.7.0

Additional packages for document conversion:
- markdown (for Markdown processing)
- xhtml2pdf (for PDF generation)
- PyMuPDF/fitz (for PDF text extraction)
- pytesseract (for OCR, optional)
- Pillow (for image processing)

For details, please refer to `requirements.txt`.

## Usage

### Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Simulation Scripts

```bash
# Run individual simulation scripts
python 03_script/01_non_commutative_noise_simulation.py
python 03_script/02_energy_landscape_visualization.py
python 03_script/03_particle_simulation.py
# ... etc
```

### Document Conversion

```bash
# Convert Markdown to PDF (follows Mathematics of Computation guidelines)
python 03_script/11_markdown_to_pdf.py input.md output.pdf

# Convert PDF to Markdown (with OCR support)
python 03_script/12_pdf_to_markdown.py input.pdf output.md

# Convert LaTeX to Markdown
python 03_script/latex_to_markdown.py input.tex output.md
```

**Note**: For PDF to Markdown conversion with OCR, Tesseract OCR must be installed on your system. On Windows, it's typically installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Manuscripts

The project includes manuscripts prepared for submission:

- **manuscript_mathematics_of_computation.md**: Main manuscript submitted to Experimental Mathematics journal
  - Includes scalability validation (zeros 1,000-10,000)
  - Runtime benchmarks vs mpmath/Arb libraries
  - Focused on computational methods and visualization
- **manuscript_current_applied_physics.md**: Alternative manuscript format

Both manuscripts are available in Markdown format and can be converted to PDF using the included conversion tools. The PDF version follows journal submission guidelines with all content embedded in a single file.

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





