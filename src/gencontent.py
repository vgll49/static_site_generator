import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            new_line = line[2:].strip()
            return new_line
    else:
        raise Exception("No H1 Header found")
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        md_file = f.read()  
        
    with open(template_path, "r", encoding="utf-8") as f:           
        template_file = f.read()
    
    headline = extract_title(md_file)
    
    html = markdown_to_html_node(md_file)
    

    html_str = html.to_html()
    new = template_file.replace("{{ Title }}", headline)
    final = new.replace("{{ Content }}", html_str)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final)
        
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)

            

