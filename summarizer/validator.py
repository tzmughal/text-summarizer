import os
from summarizer.config_manager import ConfigManager

# Load configuration
config = ConfigManager()


def validate_text(text):
    """
    Validate the input text before summarization.
    """

    if not text or not text.strip():
        raise ValueError("Input cannot be empty.")

    minimum_words = config.get("minimum_words", 20)

    if len(text.split()) < minimum_words:
        raise ValueError(
            f"Input text must contain at least {minimum_words} words for summarization."
        )


def validate_file(path):
    """
    Validate the selected input file.
    """

    if not os.path.exists(path):
        raise FileNotFoundError("File not found.")

    supported_files = config.get("supported_files", [".txt"])

    _, extension = os.path.splitext(path)

    if extension.lower() not in supported_files:
        raise ValueError(
            f"Unsupported file type '{extension}'. Supported types: {', '.join(supported_files)}"
        )