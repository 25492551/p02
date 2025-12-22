# LaTeX 설치 안내

PDF 파일을 생성하기 위해서는 LaTeX가 설치되어 있어야 합니다.

## Ubuntu/Debian 시스템

다음 명령어로 LaTeX를 설치할 수 있습니다:

```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-latex-recommended
```

## 설치 후 PDF 생성

LaTeX가 설치되면 다음 명령어로 PDF를 생성할 수 있습니다:

```bash
cd /home/seungun/project/P02
./compile_latex.sh
```

또는 직접 컴파일:

```bash
cd /home/seungun/project/P02/data
pdflatex FMP-IFC-Jan2020_submission_draft.tex
pdflatex FMP-IFC-Jan2020_submission_draft.tex  # 참조 해결을 위해 2회 실행
```

## Docker를 사용한 방법 (권한이 있는 경우)

```bash
cd /home/seungun/project/P02/data
docker run --rm -v "$(pwd):/workspace" -w /workspace texlive/texlive:latest pdflatex -interaction=nonstopmode FMP-IFC-Jan2020_submission_draft.tex
docker run --rm -v "$(pwd):/workspace" -w /workspace texlive/texlive:latest pdflatex -interaction=nonstopmode FMP-IFC-Jan2020_submission_draft.tex
```

## 온라인 LaTeX 컴파일러 사용

LaTeX를 설치할 수 없는 경우, 다음 온라인 서비스를 사용할 수 있습니다:
- Overleaf (https://www.overleaf.com)
- ShareLaTeX
- LaTeX Base

이 경우 `data/FMP-IFC-Jan2020_submission_draft.tex` 파일과 모든 그림 파일들을 업로드하여 컴파일하면 됩니다.

