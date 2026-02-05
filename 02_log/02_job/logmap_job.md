# P02 Project Job Log Map

## Job Log List

This file tracks all job logs for the P02 project.

### 2025-12-20
- Project skeleton creation
  - Basic folder structure creation (data, log, plan, report)
  - README.md writing
  - requirements.txt writing
  - plan01.md writing

### job_2025-12-21_113716.md
- **Job Date/Time**: 2025-12-21 11:37:16
- **Job Overview**: Analysis of script/8.py and detailed report writing
- **Changed Files**:
  - New: `report/08_zeta_bell_sound_synthesis_report.md`
- **Key Details**:
  - Analysis of Riemann zeta function zero-based sound synthesis algorithm
  - Analysis of generated WAV file (riemann_zeta_bell.wav, 690 KB)
  - Detailed analysis of frequency mapping, amplitude decay, non-commutative scales
  - Mathematical background and future research directions included

### job_2025-12-21_114040.md
- **Job Date/Time**: 2025-12-21 11:40:40
- **Job Overview**: Report writing for all scripts except 8.py (1.py ~ 7.py) and final report writing
- **Changed Files**:
  - New: `report/01_non_commutative_noise_simulation_report.md`
  - New: `report/02_energy_landscape_visualization_report.md`
  - New: `report/03_particle_simulation_report.md`
  - New: `report/04_vector_field_visualization_report.md`
  - New: `report/05_coulomb_gas_simulation_report.md`
  - New: `report/07_zero_prediction_report.md`
  - New: `report/00_final_report.md` (Final report)
- **Key Details**:
  - Detailed analysis reports written for each script (7 reports)
  - Final report synthesizing the entire project
  - Integrated analysis, major achievements, and future research directions included
  - Total of 8 report files created (7 individual reports + 1 final report)

### job_2025-12-22_070931.md
- **Job Date/Time**: 2025-12-22 07:09:31
- **Job Overview**: PDF to markdown conversion and LaTeX format submission draft creation
- **Changed Files**:
  - New: `script/pdf_to_markdown.py` (PDF conversion script)
  - New: `data/FMP-IFC-Jan2020.md` (Converted markdown document)
  - New: `data/FMP-IFC-Jan2020_submission_draft.tex` (LaTeX submission draft)
- **Key Details**:
  - Conversion of Forum of Mathematics, Pi journal contributor guidelines PDF to markdown
  - PDF text extraction and structuring using PyMuPDF library
  - LaTeX paper draft template creation matching journal format
  - Paper structure reflecting Riemann zeta function research content

### job_2025-12-22_073047.md
- **Job Date/Time**: 2025-12-22 07:30:47
- **Job Overview**: LaTeX submission draft completion and figure generation
- **Changed Files**:
  - Modified: `script/1.py`, `script/2.py`, `script/3.py`, `script/4.py`, `script/5.py`, `script/7.py`, `script/9.py`, `script/10.py` (Figure save path changed)
  - Modified: `data/FMP-IFC-Jan2020_submission_draft.tex` (Figure references added)
  - New: `data/FMP-IFC-Jan2020_submission_draft_todo.md` (Writing checklist)
  - New: `data/figure1_non_commutative_noise.png` ~ `data/figure8_chaos_wave.png` (Total 9 figure files)
- **Key Details**:
  - LaTeX submission draft writing checklist creation
  - Modification of all visualization scripts to save figures in data/ folder
  - Generation of 9 high-resolution figure files (300 DPI)
  - Addition of all figure references and detailed descriptions to LaTeX file
  - Paper structure completeness improvement

### job_2025-12-22_074025.md
- **Job Date/Time**: 2025-12-22 07:40:25
- **Job Overview**: Cover letter writing for Forum of Mathematics, Pi journal submission
- **Changed Files**:
  - New: `data/cover_letter.md` (Cover letter markdown file)
- **Key Details**:
  - Professional cover letter writing for journal submission
  - Originality and exclusivity confirmation included
  - Paper summary and major contributions explanation
  - Logical explanation of journal suitability
  - Conflict of interest declaration (none)
  - Submission checklist included

### job_2025-12-22_132621.md
- **Job Date/Time**: 2025-12-22 13:26:21
- **Job Overview**: File structure reorganization and .gitignore update
- **Changed Files**:
  - Modified: `.gitignore` (`data/` folder added)
  - New: `fig/` folder creation
  - Moved: `data/figure*.png` → `fig/figure*.png` (9 figure files)
- **Key Details**:
  - Structure improvement by moving figure files from `data/` to `fig/` folder
  - Addition of `data/` folder to `.gitignore` to exclude submission documents from Git tracking
  - Project structure clarification and Git repository optimization
  - File management efficiency improvement

### 20260125T152230_reconstruct_folder_structure.md
- **Job Date/Time**: 2026-01-25T152230
- **Job Overview**: Folder structure reorganization and .cursorrules update referencing ECC02 project structure
- **Changed Files**:
  - New: `.cursorrules` (Replaced with ECC02 version, integrated p02 project-specific content)
  - New: `01_data/`, `02_log/`, `03_script/`, `04_layout/`, `05_plan/`, `06_docs/` folder creation
  - Moved: `log/chat log/*` → `02_log/01_chat/`
  - Moved: `log/job log/*` → `02_log/02_job/`
  - Moved: `script/*` → `03_script/`
  - Moved: `plan/*` → `05_plan/`
  - Moved: `report/*` → `06_docs/`
  - Moved: `fig/*` → `06_docs/`
  - File name changes: Index prefix added to all script files (e.g., `1.py` → `01_.py`)
- **Key Details**:
  - Integration of ECC02 project's .cursorrules file with p02 project-specific content
  - Complete reorganization to ECC02-style folder structure with numeric prefixes
  - Integer index prefix added to all script files (ECC02 style)
  - Documents and reports integrated into `06_docs/`
  - Date/time format rules and number base notation rules added

### 20260125T152520_rename_script_files.md
- **Job Date/Time**: 2026-01-25T152520
- **Job Overview**: Addition of ECC02-style descriptive names to Python files in `03_script/` folder
- **Changed Files**:
  - File name change: `01_.py` → `01_non_commutative_noise_simulation.py`
  - File name change: `02_.py` → `02_energy_landscape_visualization.py`
  - File name change: `03_.py` → `03_particle_simulation.py`
  - File name change: `04_.py` → `04_vector_field_visualization.py`
  - File name change: `05_.py` → `05_coulomb_gas_simulation.py`
  - File name change: `07_.py` → `07_zero_prediction.py`
  - File name change: `08_.py` → `08_zeta_bell_sound_synthesis.py`
  - File name change: `09_.py` → `09_spectral_rigidity_prediction.py`
  - File name change: `10_.py` → `10_chaos_wave_prediction.py`
- **Key Details**:
  - Following ECC02 project style: `index_descriptive_name.py` format
  - Changed to names that clearly indicate each file's function
  - Function of each script can be understood from filename alone
  - Project structure consistency improvement

### 20260125T153137_translate_all_korean_to_english.md
- **Job Date/Time**: 2026-01-25T153137
- **Job Overview**: Translated all Korean content in the project to English to comply with "All English" language requirement
- **Changed Files**:
  - Translated: `05_plan/01_plan01.md` (complete translation)
  - Translated: All job log files in `02_log/02_job/` (10 files)
  - Translated: All Korean comments in 8 script files (`03_script/01_*.py` through `10_*.py`)
  - Modified: `README.md` (removed Korean poem section)
- **Key Details**:
  - All documentation files translated from Korean to English
  - All Korean comments in Python scripts translated to English
  - All Korean print statements translated to English
  - Project now fully complies with "All English" requirement in .cursorrules
  - Maintained technical accuracy and mathematical terminology
  - Code functionality unchanged

### 20260125T153820_create_manuscript_current_applied_physics.md
- **Job Date/Time**: 2026-01-25T153820
- **Job Overview**: Created comprehensive manuscript for Current Applied Physics journal submission using all details from `06_docs/` reports
- **Changed Files**:
  - New: `01_data/manuscript_current_applied_physics.md` (markdown version)
  - New: `01_data/manuscript_current_applied_physics.tex` (LaTeX version)
- **Key Details**:
  - Comprehensive manuscript (~3,500 words) incorporating all research from 10 reports
  - Includes all 8 figures with proper references
  - Complete mathematical framework and methodology sections
  - Three-step zero prediction algorithm fully documented
  - Sound synthesis methodology included
  - 10 key references from number theory and mathematical physics
  - Both markdown and LaTeX formats provided
  - Ready for author information completion

### 20260125T163525_create_manuscript_mathematics_of_computation.md
- **Job Date/Time**: 2026-01-25T163525
- **Job Overview**: Created comprehensive manuscript for Mathematics of Computation journal submission following AMS LaTeX format
- **Changed Files**:
  - New: `01_data/manuscript_mathematics_of_computation.tex` (AMS LaTeX version)
- **Key Details**:
  - Comprehensive manuscript (~4,000 words) incorporating all research from 10 reports
  - AMS LaTeX format (`amsart` document class)
  - Mathematics Subject Classification (2020 MSC): Primary 11M26; Secondary 11M06, 11M50, 37M05, 65H04, 65Y20
  - 7 formal algorithm descriptions with step-by-step procedures
  - Enhanced mathematical rigor and computational methodology focus
  - Computational complexity and numerical considerations section included
  - Abstract within 300-word limit as required
  - Ready for author information completion and submission

### 20260125T164123_convert_mathematics_of_computation_pdf_to_markdown.md
- **Job Date/Time**: 2026-01-25T164123
- **Job Overview**: Converted Mathematics of Computation journal guide PDF to markdown format
- **Changed Files**:
  - New: `01_data/Mathematics of Computation - Guide for authors.md` (converted markdown file)
- **Key Details**:
  - Used existing PDF to markdown conversion script (`03_script/12_pdf_to_markdown.py`)
  - Installed PyMuPDF library (pymupdf 1.26.7) for PDF text extraction
  - Successfully converted PDF to markdown format
  - Output file includes header with source path and conversion timestamp
  - Ready for use in documentation

### 20260125T164308_compress_job_logs.md
- **Job Date/Time**: 2026-01-25T164308
- **Job Overview**: Compressed old job log files, keeping only essential materials for future work
- **Changed Files**:
  - New: `job_logs_archive.zip` (compressed archive containing 10 old job log files)
  - Deleted: 10 old job log files (compressed into archive)
- **Key Details**:
  - Kept essential files: `logmap_job.md` and 2 most recent job logs
  - Compressed 10 old job log files into ZIP archive
  - Archive size: 13,870 bytes (~13.5 KB)
  - Folder now contains only essential files for easier management
  - All job summaries still accessible via `logmap_job.md`

### 20260205T143500_init_venv_requirements.md
- **Job Date/Time**: 2026-02-05T143500
- **Job Overview**: Initialize project locally: create venv and install requirements from requirements.txt
- **Changed Files**:
  - New: `venv/` (virtual environment)
  - New: `02_log/02_job/20260205T143500_init_venv_requirements.md`
- **Key Details**:
  - venv created with `--without-pip` (ensurepip unavailable); pip bootstrapped via get-pip.py
  - Core packages installed: numpy, matplotlib, scipy, markdown, PyMuPDF, pytesseract, Pillow, mpmath
  - xhtml2pdf not installed (requires system libcairo2-dev); optional step documented in job log
  - Activate venv: `source venv/bin/activate`

### 20260205T074743_update_duration_terminal_reporting_gpu_usage_check.md
- **Job Date/Time**: 2026-02-05T074743
- **Job Overview**: Update duration-mode logging to report key runtime info on the running terminal and add basic GPU usage checks (nvidia-smi memory/util + process GPU memory).
- **Changed Files**:
  - Modified: `03_script/16_scalability_test_gpu.py`
  - New: `02_log/02_job/20260205T074743_update_duration_terminal_reporting_gpu_usage_check.md`
- **Key Details**:
  - Implemented tee-style logger so `--duration --output ...` prints to terminal and writes to file
  - Added header diagnostics: backend, PID, Python/NumPy/CuPy versions, CUDA_VISIBLE_DEVICES, GPU device info
  - Added periodic fields: `gpu_mem_mb` and `proc_gpu_mem_mb` (best-effort via nvidia-smi)
  - Fixed datetime UTC deprecation warnings by using timezone-aware UTC timestamps

### 20260205T075514_update_usage_guide_with_terminal_gpu_usage_fields.md
- **Job Date/Time**: 2026-02-05T075514
- **Job Overview**: Update the usage guide to document tee-style duration logging and new GPU usage fields (`gpu_mem_mb`, `proc_gpu_mem_mb`).
- **Changed Files**:
  - Modified: `06_docs/11_16_scalability_test_gpu_usage.md`
  - New: `02_log/02_job/20260205T075514_update_usage_guide_with_terminal_gpu_usage_fields.md`
- **Key Details**:
  - Documented duration-mode output behavior (terminal + output file)
  - Documented header diagnostics (backend, PID, versions, CUDA_VISIBLE_DEVICES, GPU device info)
  - Documented new periodic GPU usage fields and added an example log line
  - Expanded troubleshooting guidance (pacing and sampling limitations; disable with `--util-max 0`)

## Job Log Writing Rules

1. Before starting a job: Check previous job logs
2. After completing a job: Write job log
3. Log file name format: `YYYYMMDDTHHMMSS_description.md` (ECC02 style)
4. After writing log: Update this file (logmap_job.md)

## Update Record
- 2025-12-22: job_2025-12-22_070931.md added
- 2025-12-22: job_2025-12-22_073047.md added
- 2025-12-22: job_2025-12-22_074025.md added
- 2025-12-22: job_2025-12-22_132621.md added
- 2026-01-25: 20260125T152230_reconstruct_folder_structure.md added
- 2026-01-25: 20260125T152520_rename_script_files.md added
- 2026-01-25: 20260125T153137_translate_all_korean_to_english.md added
- 2026-01-25: 20260125T153820_create_manuscript_current_applied_physics.md added
- 2026-01-25: 20260125T163525_create_manuscript_mathematics_of_computation.md added
- 2026-01-25: 20260125T164123_convert_mathematics_of_computation_pdf_to_markdown.md added
- 2026-01-25: 20260125T164308_compress_job_logs.md added
- 2026-01-25: Old job logs compressed into `job_logs_archive.zip` (10 files)
- 2026-02-05: 20260205T143500_init_venv_requirements.md added
- 2026-02-05: 20260205T074743_update_duration_terminal_reporting_gpu_usage_check.md added
- 2026-02-05: 20260205T075514_update_usage_guide_with_terminal_gpu_usage_fields.md added