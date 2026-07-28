from summarizer.summarizer_engine import TextSummarizer

text = """
Artificial Intelligence is transforming industries worldwide.

Companies use AI to automate repetitive tasks,
improve customer service,
analyze documents,
detect fraud,
and increase productivity.

Machine learning enables computers to learn from data.

Deep learning uses neural networks to solve complex problems.

Businesses continue investing billions into AI research every year.
"""

engine = TextSummarizer()

summary = engine.summarize(text, "medium")

print("\nGenerated Summary:\n")
print(summary)