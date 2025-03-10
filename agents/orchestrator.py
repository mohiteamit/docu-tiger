# agents/orchestrator.py

import os
import time
from agents.folder_scanner import get_folder_tree, find_license
from agents.file_processor import process_python_file
from agents.requirements_extractor import extract_requirements
from agents.agent_module_detail import refine_module_details
from agents.agent_requirements import refine_requirements
from agents.agent_high_level import generate_high_level_description
from docs.doc_consolidator import consolidate_documentation

def retry_agent_call(agent_func, *args, min_length=50, max_retries=2, **kwargs):
    """
    Calls the given agent function with the provided arguments and checks the output.
    If the output length is below min_length or contains an error message, re-call the agent up to max_retries times.
    """
    retries = 0
    output = agent_func(*args, **kwargs)
    while (len(output.strip()) < min_length or "No documentation generated" in output) and retries < max_retries:
        retries += 1
        time.sleep(0.5)  # slight delay before retrying
        output = agent_func(*args, **kwargs)
    return output

def orchestrate_documentation(project_folder, progress_callback=None):
    """
    Coordinates the documentation generation process.
    The progress_callback is a function accepting (progress_value, status_message).
    Returns a dictionary with individual documentation sections.
    """
    if progress_callback is None:
        progress_callback = lambda p, msg: None

    # Step 1: Scan folder structure
    progress_callback(5, "Scanning folder structure...")
    folder_structure = get_folder_tree(project_folder)
    time.sleep(0.5)

    # Step 2: Find license file (if any)
    progress_callback(10, "Searching for license file...")
    license_info = find_license(project_folder)
    time.sleep(0.5)

    # Step 3: Process Python files (ignoring noise directories)
    progress_callback(15, "Collecting Python files...")
    python_files = []
    for root, dirs, files in os.walk(project_folder):
        for d in [".git", "__pycache__", ".pytest_cache"]:
            if d in dirs:
                dirs.remove(d)
        for file in files:
            if file in ['.env', '.gitignore']:
                continue
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    total_files = len(python_files)
    modules_info = []
    for idx, file_path in enumerate(python_files, start=1):
        progress_callback(15 + int(20 * idx / total_files), f"Processing file {idx} of {total_files}: {file_path}")
        module_info = process_python_file(file_path)
        modules_info.append(module_info)
        time.sleep(0.1)

    # Step 4: Refine module details (generate descriptions from raw code)
    progress_callback(40, "Refining module and function details...")
    modules_info = refine_module_details(modules_info)
    time.sleep(0.5)

    # Step 5: Extract and refine external requirements
    progress_callback(50, "Extracting and refining requirements...")
    raw_requirements = extract_requirements(modules_info)
    requirements_section = retry_agent_call(refine_requirements, raw_requirements, project_folder, min_length=50)
    time.sleep(0.5)

    # Step 6: Consolidate module documentation section
    progress_callback(65, "Consolidating module details...")
    modules_section = ""
    for module in modules_info:
        modules_section += f"### Module: {module.get('module_name', 'Unknown')}\n"
        if 'error' in module:
            modules_section += f"Error processing module: {module['error']}\n"
        else:
            if module.get("module_description"):
                modules_section += f"**Module Description:** {module['module_description']}\n\n"
            if module.get("imports"):
                modules_section += "**Imports:** " + ", ".join(sorted(module["imports"])) + "\n\n"
            if module.get("functions"):
                for func in module["functions"]:
                    modules_section += f"- **Function: {func['function_name']}**\n"
                    modules_section += f"  - Description: {func['description']}\n"
        modules_section += "\n"
    time.sleep(0.5)
    progress_callback(75, "Module details consolidated.")

    # Step 7: Generate high-level description based on complete context
    progress_callback(80, "Generating high-level project description...")
    summary_context = f"Folder Structure:\n{folder_structure}\n\nModule Summary:\n{modules_section}"
    high_level_desc = retry_agent_call(generate_high_level_description, summary_context, min_length=50)
    time.sleep(0.5)
    progress_callback(90, "High-level description generated.")

    # Consolidate final documentation (for convenience)
    final_documentation = consolidate_documentation(
        high_level_desc,
        folder_structure,
        requirements_section,
        modules_section,
        license_info
    )
    progress_callback(100, "Documentation generation complete.")

    return {
        "folder_structure": folder_structure,
        "license_info": license_info,
        "requirements_section": requirements_section,
        "modules_section": modules_section,
        "high_level_desc": high_level_desc,
        "final_documentation": final_documentation
    }
