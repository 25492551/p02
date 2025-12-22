#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to markdown format for documentation purposes.
"""

import sys
import os
import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) not found. Installing...")
    os.system("venv/bin/pip install pymupdf")
    import fitz

def clean_text(text):
    """Clean and format text for markdown."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page breaks and form feeds
    text = re.sub(r'\f', '\n\n', text)
    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file."""
    doc = fitz.open(pdf_path)
    full_text = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        cleaned_text = clean_text(text)
        if cleaned_text:
            full_text.append(f"## Page {page_num + 1}\n\n{cleaned_text}\n")
    
    doc.close()
    return "\n".join(full_text)

def pdf_to_markdown(pdf_path, output_path):
    """Convert PDF to markdown format."""
    print(f"Converting {pdf_path} to markdown...")
    
    # Extract text from PDF
    markdown_content = extract_text_from_pdf(pdf_path)
    
    # Add header
    pdf_name = Path(pdf_path).stem
    header = f"""# {pdf_name}

**Source**: {pdf_path}
**Converted**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
    
    full_content = header + markdown_content
    
    # Write to markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Markdown file saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    # Default paths
    pdf_path = "data/FMP-IFC-Jan2020.pdf"
    output_path = "data/FMP-IFC-Jan2020.md"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    pdf_to_markdown(pdf_path, output_path)

