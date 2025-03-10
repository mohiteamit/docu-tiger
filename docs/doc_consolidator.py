# docs/doc_consolidator.py

def consolidate_documentation(high_level_desc, folder_structure, requirements_section, modules_section, license_info):
    """
    Consolidates all documentation sections into a single Markdown string.
    """
    doc_lines = []
    doc_lines.append("# Project Documentation\n")
    doc_lines.append("## High-Level Description\n")
    doc_lines.append(high_level_desc + "\n")
    
    doc_lines.append("## Folder and File Structure\n")
    doc_lines.append("```\n" + folder_structure + "\n```\n")
    
    doc_lines.append("## Requirements\n")
    doc_lines.append(requirements_section + "\n")
    
    doc_lines.append("## Modules and Functions\n")
    doc_lines.append(modules_section + "\n")
    
    doc_lines.append("## License\n")
    doc_lines.append(license_info + "\n")
    
    return "\n".join(doc_lines)
