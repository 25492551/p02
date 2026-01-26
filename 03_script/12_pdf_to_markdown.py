#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to markdown format for documentation purposes.
Supports both text-based and image-based PDFs (with OCR).
"""

import sys
import os
import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) not found. Installing...")
    os.system("pip install pymupdf")
    import fitz

# Try to import OCR libraries (optional)
OCR_AVAILABLE = False
TESSERACT_PATH = None

# Common Tesseract installation paths on Windows
WINDOWS_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME', '')),
]

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
    
    # Try to find Tesseract executable on Windows
    if sys.platform == 'win32':
        for path in WINDOWS_TESSERACT_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                TESSERACT_PATH = path
                print(f"Found Tesseract at: {path}")
                break
except ImportError:
    print("Warning: OCR libraries (pytesseract, Pillow) not available.")
    print("Attempting to install OCR dependencies...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract", "Pillow", "pdf2image"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        from PIL import Image
        import pytesseract
        OCR_AVAILABLE = True
        
        # Try to find Tesseract executable on Windows
        if sys.platform == 'win32':
            for path in WINDOWS_TESSERACT_PATHS:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    TESSERACT_PATH = path
                    print(f"Found Tesseract at: {path}")
                    break
        print("OCR libraries installed successfully.")
    except Exception as e:
        print(f"Could not install OCR libraries: {e}")
        print("For image-based PDFs, please install manually: pip install pytesseract Pillow pdf2image")
        print("Also install Tesseract OCR: https://github.com/tesseract-ocr/tesseract")

def clean_text(text):
    """Clean and format text for markdown."""
    if not text:
        return ""
    # Preserve line breaks but clean up excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove excessive spaces within lines
        cleaned_line = re.sub(r'[ \t]+', ' ', line.strip())
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    # Join lines and clean up multiple newlines
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()

def extract_text_with_ocr(page):
    """Extract text using OCR if regular extraction fails."""
    if not OCR_AVAILABLE:
        return None
    
    try:
        # Render page as image with high resolution for better OCR
        zoom = 2  # 2x zoom for better OCR accuracy
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_data = pix.tobytes("png")
        
        # Convert to PIL Image
        from io import BytesIO
        img = Image.open(BytesIO(img_data))
        
        # Perform OCR with multiple language support
        try:
            text = pytesseract.image_to_string(img, lang='eng')
        except:
            # Fallback to default language
            text = pytesseract.image_to_string(img)
        
        return text
    except Exception as e:
        print(f"Warning: OCR failed: {e}")
        print("Note: Make sure Tesseract OCR is installed on your system.")
        return None

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using multiple methods."""
    doc = fitz.open(pdf_path)
    full_text = []
    total_pages = len(doc)
    
    print(f"Processing {total_pages} pages...")
    
    for page_num in range(total_pages):
        page = doc[page_num]
        
        # Try standard text extraction first
        text = page.get_text()
        
        # If no text found, try alternative extraction methods
        if not text or len(text.strip()) < 10:
            # Try structured text extraction
            text_dict = page.get_text("dict")
            text_parts = []
            for block in text_dict.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = " ".join([span.get("text", "") for span in line.get("spans", [])])
                        if line_text.strip():
                            text_parts.append(line_text)
            text = "\n".join(text_parts)
        
        # If still no text, try OCR
        if not text or len(text.strip()) < 10:
            print(f"Page {page_num + 1}: No text found, attempting OCR...")
            ocr_text = extract_text_with_ocr(page)
            if ocr_text:
                text = ocr_text
            else:
                print(f"Page {page_num + 1}: Could not extract text (may be image-only)")
                text = f"[Page {page_num + 1}: Could not extract text - may contain only images]"
        
        cleaned_text = clean_text(text)
        if cleaned_text:
            full_text.append(f"## Page {page_num + 1}\n\n{cleaned_text}\n")
        else:
            print(f"Warning: Page {page_num + 1} produced no text after cleaning")
    
    doc.close()
    
    if not full_text:
        return "[No text could be extracted from this PDF. It may be image-based and require OCR setup.]"
    
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

