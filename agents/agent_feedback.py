# agents/agent_feedback.py

from agents.deepseek_client import deepseek_analyze

def evaluate_feedback(section_type, original_text, feedback_text):
    """
    Evaluates the user feedback for a given section and returns a revised version of that section.
    section_type can be "high_level", "modules", or "requirements".
    """
    prompt = (
        f"The following is the original {section_type} documentation:\n\n{original_text}\n\n"
        f"User feedback: {feedback_text}\n\n"
        f"Based on this feedback, generate an improved version of the {section_type} documentation. "
        f"Ensure the new version addresses the user's concerns."
    )
    revised_text = deepseek_analyze(prompt)
    return revised_text
