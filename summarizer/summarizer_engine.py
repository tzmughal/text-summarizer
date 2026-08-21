import re
from nltk.tokenize import sent_tokenize

from summarizer.model_loader import ModelLoader
from summarizer.config_manager import ConfigManager


class TextSummarizer:
    """
    Handles text summarization using the locally stored AI model.
    """

    def __init__(self):
        self.model = ModelLoader.get_model()
        self.config = ConfigManager()

    def summarize(self, text, length="medium"):
        """
        Generate a summary.

        Parameters:
            text (str): Input text
            length (str): short, medium, or long

        Returns:
            str: Generated summary
        """

        # Count input words
        input_words = len(text.split())

        # Load summary ratios from config.json
        ratios = self.config.get("summary_lengths", {})

        # Default summary length
        default_length = self.config.get("default_summary", "medium")

        if length not in ratios:
            length = default_length

        ratio = ratios.get(length, 0.40)

        # Calculate summary size
        max_length = max(40, int(input_words * ratio) + 10)
        min_length = max(20, int(max_length * 0.6))

        # Prevent max_length from exceeding input size
        if max_length >= input_words:
            max_length = max(20, input_words - 5)

        # Ensure min_length is always smaller than max_length
        if min_length >= max_length:
            min_length = max(10, max_length // 2)

        # Generate summary
        result = self.model(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=False,
            truncation=True
        )

        summary = result[0].get("summary_text") or result[0].get("generated_text", "")

        # Remove spaces before punctuation
        summary = re.sub(r"\s+([.,!?;:])", r"\1", summary)

        # Collapse multiple spaces
        summary = re.sub(r"\s+", " ", summary)

        summary = summary.strip()

        # Remove unfinished ending punctuation
        summary = summary.rstrip(",;:")

        # Trim incomplete sentences using sentence tokenization
        try:
            sentences = sent_tokenize(summary)
            if sentences:
                # Keep only complete sentences (those ending with proper punctuation)
                complete_sentences = []
                for sent in sentences:
                    sent = sent.strip()
                    if sent and sent[-1] in ".!?":
                        complete_sentences.append(sent)
                
                if complete_sentences:
                    summary = " ".join(complete_sentences)
                elif sentences:
                    # If no complete sentences, use the first sentence and ensure it ends with a period
                    summary = sentences[0].strip()
                    if summary and summary[-1] not in ".!?":
                        summary += "."
        except Exception:
            # Fallback if sent_tokenize fails
            if summary and summary[-1] not in ".!?":
                summary += "."

        return summary