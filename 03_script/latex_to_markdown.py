#!/usr/bin/env python3
"""
LaTeX to Markdown Converter
Converts LaTeX files to markdown format.
"""

import sys
import os
import re
from pathlib import Path

def convert_latex_to_markdown(tex_content):
    """Convert LaTeX content to markdown."""
    
    # Remove document class and packages
    tex_content = re.sub(r'\\documentclass\[.*?\]\{.*?\}\n', '', tex_content)
    tex_content = re.sub(r'\\documentclass\{.*?\}\n', '', tex_content)
    tex_content = re.sub(r'\\usepackage\[.*?\]\{.*?\}\n', '', tex_content)
    tex_content = re.sub(r'\\usepackage\{.*?\}\n', '', tex_content)
    tex_content = re.sub(r'\\geometry\{.*?\}\n', '', tex_content)
    
    # Handle subject classification
    tex_content = re.sub(r'% Mathematics Subject Classification.*?\n', '', tex_content)
    tex_content = re.sub(r'\\subjclass\[2020\]\{([^}]+)\}', r'**Mathematics Subject Classification (2020)**: \1', tex_content)
    
    # Handle title
    tex_content = re.sub(r'\\title\[([^\]]+)\]\{([^}]+)\}', r'# \2', tex_content)
    tex_content = re.sub(r'\\title\{([^}]+)\}', r'# \1', tex_content)
    
    # Handle authors - collect all authors first
    authors = []
    author_matches = list(re.finditer(r'\\author\{([^}]+)\}', tex_content))
    for match in author_matches:
        authors.append(match.group(1))
    
    # Remove author, address, email blocks
    tex_content = re.sub(r'\\author\{[^}]+\}', '', tex_content)
    tex_content = re.sub(r'\\address\{[^}]+\}', '', tex_content)
    tex_content = re.sub(r'\\email\{[^}]+\}', '', tex_content)
    
    # Insert authors after title
    if authors:
        authors_text = '\n\n**Authors**: ' + ', '.join(authors) + '\n'
        title_match = re.search(r'^# .+', tex_content, re.MULTILINE)
        if title_match:
            pos = title_match.end()
            tex_content = tex_content[:pos] + authors_text + tex_content[pos:]
    
    # Handle keywords
    tex_content = re.sub(r'\\keywords\{([^}]+)\}', r'\n\n**Keywords**: \1\n', tex_content)
    
    # Handle date
    tex_content = re.sub(r'\\date\{([^}]+)\}', r'\n**Date**: \1\n', tex_content)
    tex_content = re.sub(r'\\date\{\\today\}', '', tex_content)
    
    # Remove begin/end document
    tex_content = re.sub(r'\\begin\{document\}', '', tex_content)
    tex_content = re.sub(r'\\end\{document\}', '', tex_content)
    
    # Handle abstract
    tex_content = re.sub(r'\\begin\{abstract\}', '\n## Abstract\n\n', tex_content)
    tex_content = re.sub(r'\\end\{abstract\}', '\n', tex_content)
    
    # Handle maketitle
    tex_content = re.sub(r'\\maketitle', '', tex_content)
    
    # Handle sections
    tex_content = re.sub(r'\\section\*\{([^}]+)\}', r'\n## \1\n', tex_content)
    tex_content = re.sub(r'\\section\{([^}]+)\}', r'\n## \1\n', tex_content)
    tex_content = re.sub(r'\\subsection\*\{([^}]+)\}', r'\n### \1\n', tex_content)
    tex_content = re.sub(r'\\subsection\{([^}]+)\}', r'\n### \1\n', tex_content)
    tex_content = re.sub(r'\\subsubsection\{([^}]+)\}', r'\n#### \1\n', tex_content)
    
    # Handle equations - keep LaTeX math syntax
    tex_content = re.sub(r'\\begin\{equation\}', '\n$$\n', tex_content)
    tex_content = re.sub(r'\\end\{equation\}', '\n$$\n', tex_content)
    tex_content = re.sub(r'\\begin\{align\}', '\n$$\n\\\\begin{align}', tex_content)
    tex_content = re.sub(r'\\end\{align\}', '\\\\end{align}\n$$\n', tex_content)
    
    # Handle itemize and enumerate - process block by block
    def process_list_block(match):
        list_type = match.group(1)
        content = match.group(2)
        
        if list_type == 'enumerate':
            # Numbered list
            items = re.findall(r'\\item\s+(.*?)(?=\\item|$)', content, re.DOTALL)
            result = []
            for i, item in enumerate(items, 1):
                cleaned_item = item.strip().replace('\n', ' ')
                result.append(f'{i}. {cleaned_item}')
            return '\n' + '\n'.join(result) + '\n'
        else:  # itemize
            # Bullet list
            items = re.findall(r'\\item\s+(.*?)(?=\\item|$)', content, re.DOTALL)
            result = []
            for item in items:
                cleaned_item = item.strip().replace('\n', ' ')
                result.append(f'- {cleaned_item}')
            return '\n' + '\n'.join(result) + '\n'
    
    # Process enumerate blocks
    tex_content = re.sub(
        r'\\begin\{(enumerate)\}(.*?)\\end\{enumerate\}',
        process_list_block,
        tex_content,
        flags=re.DOTALL
    )
    
    # Process itemize blocks
    tex_content = re.sub(
        r'\\begin\{(itemize)\}(.*?)\\end\{itemize\}',
        process_list_block,
        tex_content,
        flags=re.DOTALL
    )
    
    # Handle citations
    tex_content = re.sub(r'\\cite\{([^}]+)\}', r'[@\1]', tex_content)
    
    # Handle bibliography
    tex_content = re.sub(r'\\begin\{thebibliography\}\{.*?\}', '\n## References\n\n', tex_content)
    tex_content = re.sub(r'\\end\{thebibliography\}', '', tex_content)
    
    # Handle bibitem - convert to markdown format
    def process_bibitem(match):
        key = match.group(1)
        content = match.group(2).strip()
        # Clean up LaTeX formatting in bibliography
        content = re.sub(r'\\textit\{([^}]+)\}', r'*\1*', content)
        return f'\n**[{key}]** {content}\n'
    
    tex_content = re.sub(
        r'\\bibitem\{([^}]+)\}\s+(.*?)(?=\\bibitem|\\end|$)',
        process_bibitem,
        tex_content,
        flags=re.DOTALL
    )
    
    # Handle textbf (bold)
    tex_content = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', tex_content)
    
    # Handle textit (italic)
    tex_content = re.sub(r'\\textit\{([^}]+)\}', r'*\1*', tex_content)
    
    # Handle texttt (monospace)
    tex_content = re.sub(r'\\texttt\{([^}]+)\}', r'`\1`', tex_content)
    
    # Clean up multiple blank lines
    tex_content = re.sub(r'\n{3,}', '\n\n', tex_content)
    
    # Clean up leading/trailing whitespace
    tex_content = tex_content.strip()
    
    return tex_content

def latex_to_markdown(tex_path, output_path):
    """Convert LaTeX file to markdown."""
    print(f"Converting {tex_path} to markdown...")
    
    # Read LaTeX file
    with open(tex_path, 'r', encoding='utf-8') as f:
        tex_content = f.read()
    
    # Convert to markdown
    markdown_content = convert_latex_to_markdown(tex_content)
    
    # Add header
    tex_name = Path(tex_path).stem
    header = f"""# {tex_name}

**Source**: {tex_path}
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
    tex_path = "data/manuscript.tex"
    output_path = "data/manuscript.md"
    
    if len(sys.argv) > 1:
        tex_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Auto-generate output path
        output_path = str(Path(tex_path).with_suffix('.md'))
    
    if not os.path.exists(tex_path):
        print(f"Error: LaTeX file not found: {tex_path}")
        sys.exit(1)
    
    latex_to_markdown(tex_path, output_path)
