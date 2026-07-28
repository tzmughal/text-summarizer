# test_file.py

from summarizer.file_handler import read_text_file

text = read_text_file("sample_inputs/sample1.txt")

print(text)