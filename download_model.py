from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from summarizer.config_manager import ConfigManager

config = ConfigManager()
MODEL_NAME = config.get("model_name", "sshleifer/distilbart-cnn-12-6")
SAVE_PATH = config.get("model_path", "./models/distilbart-cnn-12-6")

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Downloading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Saving model locally...")
tokenizer.save_pretrained(SAVE_PATH)
model.save_pretrained(SAVE_PATH)

print(f"Model saved to: {SAVE_PATH}")