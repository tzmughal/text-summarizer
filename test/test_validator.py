# test_validator.py

from summarizer.validator import validate_text

text = input("Enter text: ")

try:
    validate_text(text)
    print("Validation Passed")

except Exception as e:
    print("Error:", e)