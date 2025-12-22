#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts markdown files to PDF format.
"""

import sys
import os
from pathlib import Path

try:
    import markdown
    from weasyprint import HTML, CSS
except ImportError:
    print("Required packages not found. Installing...")
    os.system("venv/bin/pip install markdown weasyprint")
    import markdown
    from weasyprint import HTML, CSS

def markdown_to_pdf(md_path, pdf_path, title="Document"):
    """Convert markdown file to PDF."""
    print(f"Converting {md_path} to PDF...")
    
    # Read markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # Add CSS styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #000;
            }}
            h1 {{
                font-size: 18pt;
                font-weight: bold;
                margin-top: 1em;
                margin-bottom: 0.5em;
                border-bottom: 2px solid #000;
                padding-bottom: 0.3em;
            }}
            h2 {{
                font-size: 16pt;
                font-weight: bold;
                margin-top: 1em;
                margin-bottom: 0.5em;
                border-bottom: 1px solid #666;
                padding-bottom: 0.2em;
            }}
            h3 {{
                font-size: 14pt;
                font-weight: bold;
                margin-top: 0.8em;
                margin-bottom: 0.4em;
            }}
            p {{
                margin: 0.5em 0;
                text-align: justify;
            }}
            ul, ol {{
                margin: 0.5em 0;
                padding-left: 2em;
            }}
            li {{
                margin: 0.3em 0;
            }}
            strong {{
                font-weight: bold;
            }}
            em {{
                font-style: italic;
            }}
            code {{
                font-family: 'Courier New', monospace;
                font-size: 10pt;
                background-color: #f5f5f5;
                padding: 2px 4px;
                border-radius: 3px;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 1em;
                border-radius: 5px;
                overflow-x: auto;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ccc;
                margin: 1em 0;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=html_template).write_pdf(pdf_path)
    
    print(f"PDF file saved to: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    # Default paths
    md_path = "data/cover_letter.md"
    pdf_path = "data/cover_letter.pdf"
    
    if len(sys.argv) > 1:
        md_path = sys.argv[1]
    if len(sys.argv) > 2:
        pdf_path = sys.argv[2]
    
    if not os.path.exists(md_path):
        print(f"Error: Markdown file not found: {md_path}")
        sys.exit(1)
    
    title = Path(md_path).stem.replace('_', ' ').title()
    markdown_to_pdf(md_path, pdf_path, title)

