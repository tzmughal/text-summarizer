import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from summarizer.config_manager import ConfigManager


class ModelLoader:
    """
    Loads the summarization model only once.
    """

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            config = ConfigManager()

            model_path = config.get("model_path", "./models/distilbart-cnn-12-6")

            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model not found at '{model_path}'. "
                    "Run download_model.py first."
                )

            print("Loading AI model...")

            # Load tokenizer and model directly for Transformers v5+ compatibility
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            
            # Use custom wrapper for consistent interface across v4 and v5+
            cls._model = SummarizationWrapper(model, tokenizer)

            print("Model loaded successfully.\n")

        return cls._model


class SummarizationWrapper:
    """Wrapper for Seq2Seq models to provide a consistent summarization interface."""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def __call__(self, texts, min_length=20, max_length=100, **kwargs):
        """Generate summaries for input texts."""
        if isinstance(texts, str):
            texts = [texts]
        
        # Filter out unsupported kwargs
        supported_kwargs = {
            'num_beams', 'early_stopping', 'length_penalty', 
            'do_sample', 'temperature', 'top_p', 'top_k', 'repetition_penalty'
        }
        generate_kwargs = {k: v for k, v in kwargs.items() if k in supported_kwargs}
        
        results = []
        for text in texts:
            # Tokenize input
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            )
            
            # Generate summary
            summary_ids = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs.get("attention_mask"),
                min_length=min_length,
                max_length=max_length,
                **generate_kwargs
            )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            results.append({"summary_text": summary})
        
        # Always return list for consistency
        return results