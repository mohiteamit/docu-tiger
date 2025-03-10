# agents/requirements_extractor.py

def extract_requirements(modules_info):
    """
    Consolidates all imported modules from modules_info into a raw set.
    """
    requirements = set()
    for module in modules_info:
        requirements.update(module.get("imports", set()))
    return requirements
