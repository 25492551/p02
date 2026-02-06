# Job Log: Manuscript Large Batch Results and Figure Regeneration

- **Job Date/Time**: 2026-02-06T120000
- **Job Overview**: Updated submission manuscript with large batch GPU calculation results and recreated all submission figures in `06_docs` (images were not pulled previously due to old gitignore).

## Changed Files

- **Modified**: `01_data/submission/manuscript_mathematics_of_computation.md`
  - Added large batch GPU validation: 3-hour run, 570,643,095 zeros (CuPy GPU, batch 100,000), mean 0.001 ms/zero, mean relative error 0.0312%, max 7.08%.
  - Cited `06_docs/gpu_scalability_3h_lightlog_util87_20260205T171511.txt`.
  - Updated Abstract and "Scalability Validation" / "Prediction Accuracy and Scalability" with 570M-zeros run.
- **Modified**: `03_script/15_generate_all_figures.py`
  - Added comment for Figure 9 referencing the large batch GPU log.
- **New (regenerated)**: `06_docs/figure1_non_commutative_noise.png` through `06_docs/figure10_benchmark_comparison.png` (10 figures).

## Key Details

- **Large batch source**: `06_docs/gpu_scalability_3h_lightlog_util87_20260205T171511.txt` (3-hour duration run, 28,545 runs, 570,643,095 zeros, err_mean% 0.0312, ms/zero 0.001).
- **Figure regeneration**: Ran `03_script/15_generate_all_figures.py` from project root; all 10 figures saved to `06_docs/` at 300 DPI for submission manuscript.
- Manuscript figure paths unchanged: `../06_docs/figure*.png` from `01_data/submission/`.

## Update Record

- 2026-02-06: Job completed; log and logmap updated.
