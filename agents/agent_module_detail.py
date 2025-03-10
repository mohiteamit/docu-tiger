# agents/agent_module_detail.py

from agents.deepseek_client import deepseek_analyze

def refine_module_details(modules_info):
    """
    For each module, generate a module-level description and for each function, generate a description using Deepseek.
    All descriptions are generated solely from the raw code.
    """
    for module in modules_info:
        # Generate module description from the full module code.
        module_code = module.get("module_code", "")
        module_prompt = (
            f"Analyze the following Python module code and generate a clear, concise description of its purpose, functionality, and key components. "
            f"Use only the code provided.\n\n{module_code}"
        )
        module_description = deepseek_analyze(module_prompt)
        module["module_description"] = module_description
        
        refined_functions = []
        for func in module.get("functions", []):
            raw_code = func.get("raw_code", "")
            prompt = (
                f"Analyze the following Python function code and generate a clear and concise description of its functionality, including its purpose, parameters, and usage. "
                f"Do not rely on any existing comments or docstrings; use only the code provided.\n\n{raw_code}"
            )
            new_desc = deepseek_analyze(prompt)
            func["description"] = new_desc
            refined_functions.append(func)
        module["functions"] = refined_functions
    return modules_info
