#!/bin/bash
# LaTeX 컴파일 스크립트
# 사용법: ./compile_latex.sh

cd "$(dirname "$0")/data"

# LaTeX 컴파일 (2회 실행하여 참조 해결)
pdflatex -interaction=nonstopmode FMP-IFC-Jan2020_submission_draft.tex
pdflatex -interaction=nonstopmode FMP-IFC-Jan2020_submission_draft.tex

# 생성된 PDF 확인
if [ -f "FMP-IFC-Jan2020_submission_draft.pdf" ]; then
    echo "PDF 생성 완료: data/FMP-IFC-Jan2020_submission_draft.pdf"
    ls -lh FMP-IFC-Jan2020_submission_draft.pdf
else
    echo "PDF 생성 실패. 로그 파일을 확인하세요."
    exit 1
fi

