import sys
import PyPDF2
import re

def pdf_to_markdown(pdf_path, markdown_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        with open(markdown_path, 'w', encoding='utf-8') as md_file:
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text = page.extract_text()
                
                text = re.sub(r'\n{3,}', '\n\n', text)
                
                lines = text.split('\n')
                formatted_lines = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        formatted_lines.append('')
                        continue
                        
                    if line.isupper() or (line.endswith(':') and len(line) < 50):
                        formatted_lines.append(f'## {line}')
                    else:
                        formatted_lines.append(line)
                
                formatted_text = '\n'.join(formatted_lines)
                
                if i < len(reader.pages) - 1:
                    formatted_text += '\n\n---\n\n'
                
                md_file.write(formatted_text)
    
    print(f"Conversion complete. Markdown file saved to: {markdown_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input.pdf output.md")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    markdown_path = sys.argv[2]
    
    pdf_to_markdown(pdf_path, markdown_path)

if __name__ == '__main__':
    main()
