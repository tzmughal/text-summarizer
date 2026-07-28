import json
import os


def save_summary(original_text, summary, output_file):

    data = {

        "original_text": original_text,

        "summary": summary

    }

    os.makedirs("sample_outputs", exist_ok=True)

    path = os.path.join("sample_outputs", output_file)

    with open(path, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)

    print(f"\nSaved to {path}")