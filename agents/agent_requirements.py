# agents/agent_requirements.py

from agents.deepseek_client import deepseek_analyze

def refine_requirements(raw_requirements, project_folder):
    """
    Refines the raw list of imported modules into a list of external dependencies.
    Excludes modules that are internal to the project.
    """
    raw_list = sorted(list(raw_requirements))
    prompt = (
        f"The following is a list of imported modules from a Python project: {raw_list}.\n"
        f"Exclude any modules that are part of the project (internal modules) and list only the external dependencies that need to be installed. "
        f"Return the refined list as Markdown bullet points."
    )
    return deepseek_analyze(prompt)
