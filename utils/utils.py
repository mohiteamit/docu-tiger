# utils/utils.py

def chunk_text(text, max_length=1000):
    """
    Splits the given text into chunks of maximum length.
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]
