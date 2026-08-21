# Local AI Text Summarization Tool

A Python-based desktop application that generates concise summaries from user-provided text or TXT files using a locally stored Hugging Face Transformer model. The application runs locally after the model has been downloaded once, allowing users to create summaries without relying on cloud services or paid APIs.

---

## Project Overview

The Local AI Text Summarization Tool makes long documents easier to review by generating meaningful summaries while preserving the main ideas. Users can paste text directly into the app, load a TXT file, choose a summary length, and save the output as JSON.

The project uses a modular structure with separate components for preprocessing, validation, configuration, model loading, and summary generation.

---

## Features

- Desktop GUI built with Tkinter
- Paste text directly into the input box
- Load TXT files through a file browser
- Choose Short, Medium, or Long summary lengths
- Automatic text preprocessing
- Input validation and error handling
- Save summaries as JSON files
- Local/offline summarization after the model is downloaded
- Background processing so the GUI stays responsive
- Progress bar and status updates during summarization
- Time taken display for each summary run
- Configurable settings through config.json
- Example script for quick command-line usage

---

## Technologies Used

- Python 3.11
- Tkinter
- Hugging Face Transformers
- PyTorch
- NLTK
- JSON

---

## Project Structure

```text
TextSummarizer/
├── app.py
├── config.json
├── download_model.py
├── example_usage.py
├── README.md
├── requirements.txt
├── models/
│   └── distilbart-cnn-12-6/
├── sample_inputs/
│   ├── ai.txt
│   ├── climate_change.txt
│   ├── healthcare.txt
│   └── sample1.txt
├── sample_outputs/
│   ├── summary.json
│   └── summary-medium.json
└── summarizer/
    ├── __init__.py
    ├── config_manager.py
    ├── file_handler.py
    ├── model_loader.py
    ├── output.py
    ├── preprocessing.py
    ├── summarizer_engine.py
    └── validator.py
```

---

## Requirements

- Python 3.11
- Windows, Linux, or macOS
- Internet connection only once to download the model

Install requirements with:

```bash
pip install -r requirements.txt
```

---

## Installation

1. Open a terminal in the project folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Download the model once:

```bash
python download_model.py
```

The model will be stored in the models directory.

---

## How to Run

### 1. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the Model (First Time Only)

```bash
python download_model.py
```

### 4. Run the Application

#### Desktop App

```bash
python app.py
```

#### Example Script

```bash
python example_usage.py
```

### 5. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

---

## Using the Application

### Option 1: Paste Text

1. Launch the application.
2. Paste or type text into the input box.
3. Choose a summary length.
4. Click Generate Summary.
5. Review the generated summary.
6. Save it as JSON if needed.

### Option 2: Load a TXT File

1. Click Browse TXT File.
2. Select a TXT file.
3. Choose Short, Medium, or Long.
4. Click Generate Summary.
5. Review the output.
6. Save the result as JSON.

---

## Configuration

Application settings are stored in config.json.

Example configuration:

```json
{
    "model_path": "./models/distilbart-cnn-12-6",
    "model_name": "sshleifer/distilbart-cnn-12-6",
    "pipeline_task": "text2text-generation",
    "supported_files": [".txt"],
    "default_summary": "medium",
    "summary_lengths": {
        "short": 0.25,
        "medium": 0.40,
        "long": 0.60
    },
    "minimum_words": 10,
    "example_input_file": "sample_inputs/ai.txt",
    "example_summary_length": "medium",
    "window_title": "Local AI Text Summarizer",
    "window_size": {
        "width": 1000,
        "height": 800
    },
    "window_min_size": {
        "width": 900,
        "height": 700
    },
    "progress_interval": 12
}
```

You can change:

- Model location and model name
- Default summary length
- Summary ratios
- Minimum word count
- Supported file extensions
- Window size and title
- Progress bar timing

---

## Error Handling

The app handles common issues such as:

- Empty input text
- Too-short input text
- Missing files
- Unsupported file types
- Model loading issues
- JSON export errors

Error messages are shown through dialog boxes, and the GUI remains responsive while summarization runs.

---

## Offline Execution

The summarization workflow is performed locally.

- Internet access is needed only once to download the model.
- The model is stored in the models directory.
- Later runs work offline without any cloud service dependency.

---

## Sample Files

Example input documents are included in sample_inputs/.

Included files:

- ai.txt
- climate_change.txt
- healthcare.txt
- sample1.txt

Example summaries are included in sample_outputs/.

Included files:

- summary.json
- summary-medium.json

