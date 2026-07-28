from summarizer.config_manager import ConfigManager
from summarizer.file_handler import read_txt
from summarizer.validator import validate_text
from summarizer.summarizer_engine import TextSummarizer

try:
    config = ConfigManager()
    input_file = config.get("example_input_file", "sample_inputs/ai.txt")
    summary_length = config.get("example_summary_length", "medium")

    text = read_txt(input_file)

    validate_text(text)

    summarizer = TextSummarizer()

    summary = summarizer.summarize(text, summary_length)

    print(summary)
except FileNotFoundError as e:
    print(f"Error: File not found - {e}")
    exit(1)
except ValueError as e:
    print(f"Validation Error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)