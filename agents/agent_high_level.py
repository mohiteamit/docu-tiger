# agents/agent_high_level.py

from agents.deepseek_client import deepseek_analyze

def generate_high_level_description(context):
    """
    Generates a high-level project description based on the provided context.
    """
    prompt = (
        f"Using the following information about a Python project, provide a high-level project description that summarizes the overall purpose, design, and components. "
        f"Do not simply restate details; provide an insightful overview.\n\n{context}"
    )
    return deepseek_analyze(prompt)
