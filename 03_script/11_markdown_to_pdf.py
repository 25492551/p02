#!/usr/bin/env python3
"""
Markdown to PDF Converter
Converts markdown files to PDF format.
Follows Mathematics of Computation guidelines: All text and images in one PDF file.
"""

import sys
import os
import re
import html
from pathlib import Path

try:
    import markdown
    from xhtml2pdf import pisa
    from io import BytesIO
except ImportError:
    print("Required packages not found. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "xhtml2pdf"])
    import markdown
    from xhtml2pdf import pisa
    from io import BytesIO

def format_math_for_display(math_content):
    """Format LaTeX math content for better human readability."""
    # Clean up whitespace
    math_content = math_content.strip()
    
    # Improve spacing around operators
    math_content = re.sub(r'\s*=\s*', ' = ', math_content)
    math_content = re.sub(r'\s*\+\s*', ' + ', math_content)
    math_content = re.sub(r'\s*-\s*', ' - ', math_content)
    math_content = re.sub(r'\s*\*\s*', ' × ', math_content)  # Use × for multiplication
    math_content = re.sub(r'\s*/\s*', ' / ', math_content)
    math_content = re.sub(r'\s*\\leq\s*', ' ≤ ', math_content)
    math_content = re.sub(r'\s*\\geq\s*', ' ≥ ', math_content)
    math_content = re.sub(r'\s*\\neq\s*', ' ≠ ', math_content)
    math_content = re.sub(r'\s*\\approx\s*', ' ≈ ', math_content)
    
    # Improve spacing around common functions
    math_content = re.sub(r'\\log\s*', 'log ', math_content)
    math_content = re.sub(r'\\sin\s*', 'sin ', math_content)
    math_content = re.sub(r'\\cos\s*', 'cos ', math_content)
    math_content = re.sub(r'\\exp\s*', 'exp ', math_content)
    math_content = re.sub(r'\\sum\s*', '∑ ', math_content)
    math_content = re.sub(r'\\prod\s*', '∏ ', math_content)
    math_content = re.sub(r'\\int\s*', '∫ ', math_content)
    
    # Improve Greek letters readability
    math_content = re.sub(r'\\alpha', 'α', math_content)
    math_content = re.sub(r'\\beta', 'β', math_content)
    math_content = re.sub(r'\\gamma', 'γ', math_content)
    math_content = re.sub(r'\\delta', 'δ', math_content)
    math_content = re.sub(r'\\epsilon', 'ε', math_content)
    math_content = re.sub(r'\\zeta', 'ζ', math_content)
    math_content = re.sub(r'\\theta', 'θ', math_content)
    math_content = re.sub(r'\\pi', 'π', math_content)
    math_content = re.sub(r'\\sigma', 'σ', math_content)
    math_content = re.sub(r'\\Gamma', 'Γ', math_content)
    math_content = re.sub(r'\\Delta', 'Δ', math_content)
    math_content = re.sub(r'\\Sigma', 'Σ', math_content)
    
    # Improve subscripts and superscripts spacing
    math_content = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', math_content)
    math_content = re.sub(r'\^\{([^}]+)\}', r'<sup>\1</sup>', math_content)
    math_content = re.sub(r'_([a-zA-Z0-9])', r'<sub>\1</sub>', math_content)
    math_content = re.sub(r'\^([a-zA-Z0-9])', r'<sup>\1</sup>', math_content)
    
    # Improve fractions
    math_content = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)', math_content)
    
    # Improve spacing around parentheses
    math_content = re.sub(r'\\left\(', '(', math_content)
    math_content = re.sub(r'\\right\)', ')', math_content)
    math_content = re.sub(r'\\left\[', '[', math_content)
    math_content = re.sub(r'\\right\]', ']', math_content)
    
    # Clean up multiple spaces
    math_content = re.sub(r'\s+', ' ', math_content)
    
    return math_content.strip()

def process_math_expressions(content):
    """Process LaTeX math expressions in HTML content with improved visualization."""
    # Process both markdown source and HTML content
    # Convert block math $$...$$ to HTML with proper formatting
    def replace_block_math(match):
        math_content = match.group(1).strip()
        # Format for better readability
        formatted_math = format_math_for_display(math_content)
        # Escape HTML special characters but preserve sub/sup tags
        formatted_math = html.escape(formatted_math)
        # Restore HTML tags after escaping
        formatted_math = formatted_math.replace('&lt;sub&gt;', '<sub>').replace('&lt;/sub&gt;', '</sub>')
        formatted_math = formatted_math.replace('&lt;sup&gt;', '<sup>').replace('&lt;/sup&gt;', '</sup>')
        return f'<div class="math-block">{formatted_math}</div>'
    
    # Convert inline math $...$ to HTML
    def replace_inline_math(match):
        math_content = match.group(1).strip()
        # Format for better readability
        formatted_math = format_math_for_display(math_content)
        formatted_math = html.escape(formatted_math)
        formatted_math = formatted_math.replace('&lt;sub&gt;', '<sub>').replace('&lt;/sub&gt;', '</sub>')
        formatted_math = formatted_math.replace('&lt;sup&gt;', '<sup>').replace('&lt;/sup&gt;', '</sup>')
        return f'<span class="math-inline">{formatted_math}</span>'
    
    # Process block math ($$...$$) - handle both markdown and HTML
    content = re.sub(r'\$\$\s*\n?(.*?)\n?\s*\$\$', replace_block_math, content, flags=re.DOTALL)
    content = re.sub(r'<div class="math-block">\$\$(.*?)\$\$</div>', replace_block_math, content, flags=re.DOTALL)
    
    # Process inline math ($...$) - but not block math
    content = re.sub(r'(?<!\$)\$(?!\$)([^$\n<>]+?)\$(?!\$)', replace_inline_math, content)
    
    return content

def process_images(md_content, md_path):
    """Process image references and embed them in HTML."""
    md_dir = Path(md_path).parent
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # Resolve relative paths
        if not os.path.isabs(img_path):
            img_path = md_dir / img_path
        else:
            img_path = Path(img_path)
        
        if img_path.exists():
            # Convert image to base64 for embedding (ensures all content in one PDF)
            import base64
            with open(img_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                img_ext = img_path.suffix.lower()
                mime_type = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml'
                }.get(img_ext, 'image/png')
                return f'<img src="data:{mime_type};base64,{img_data}" alt="{alt_text}" class="embedded-image" />'
        else:
            print(f"Warning: Image not found: {img_path}")
            return f'<p class="missing-image">[Image not found: {img_path}]</p>'
    
    # Process markdown image syntax ![alt](path)
    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, md_content)
    
    return md_content

def markdown_to_pdf(md_path, pdf_path, title="Document"):
    """Convert markdown file to PDF following Mathematics of Computation guidelines."""
    print(f"Converting {md_path} to PDF...")
    print("Following guide: All text and images in one PDF file")
    
    # Read markdown file
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Process images before markdown conversion
    md_content = process_images(md_content, md_path)
    
    # Convert markdown to HTML first
    html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    # Process math expressions after markdown conversion to preserve HTML formatting
    html_content = process_math_expressions(html_content)
    
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
            .math-block {{
                text-align: center;
                margin: 1.5em 0;
                padding: 1em;
                font-family: 'Times New Roman', serif;
                font-size: 13pt;
                line-height: 1.6;
                background-color: #fafafa;
                border-left: 4px solid #0066cc;
                border-radius: 4px;
                white-space: pre-wrap;
                word-spacing: 0.2em;
            }}
            .math-inline {{
                font-family: 'Times New Roman', serif;
                font-style: italic;
                font-size: 12pt;
                padding: 0.1em 0.2em;
                background-color: #f5f5f5;
                border-radius: 3px;
            }}
            .math-block sub, .math-inline sub {{
                font-size: 0.75em;
                vertical-align: sub;
                line-height: 0;
            }}
            .math-block sup, .math-inline sup {{
                font-size: 0.75em;
                vertical-align: super;
                line-height: 0;
            }}
            .embedded-image {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 1em auto;
                page-break-inside: avoid;
            }}
            .missing-image {{
                color: #cc0000;
                font-style: italic;
                border: 1px dashed #cc0000;
                padding: 0.5em;
            }}
            /* Ensure all content stays together */
            p, div, h1, h2, h3, h4, h5, h6 {{
                page-break-inside: avoid;
                orphans: 3;
                widows: 3;
            }}
            /* Mathematics of Computation style: 12pt, double-spaced equivalent */
            body {{
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.8; /* Approximately double-spaced */
                color: #000;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to PDF using xhtml2pdf
    result_file = open(pdf_path, "w+b")
    pisa_status = pisa.CreatePDF(
        BytesIO(html_template.encode('utf-8')),
        dest=result_file,
        encoding='utf-8'
    )
    result_file.close()
    
    if pisa_status.err:
        print(f"Error creating PDF: {pisa_status.err}")
        return None
    
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

