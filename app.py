import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from summarizer.config_manager import ConfigManager
from summarizer.file_handler import read_txt
from summarizer.preprocessing import clean_text, word_count
from summarizer.validator import validate_text, validate_file
from summarizer.summarizer_engine import TextSummarizer


class TextSummarizerApp:

    def __init__(self, root):
        self.root = root
        self.config = ConfigManager()

        window_title = self.config.get("window_title", "Local AI Text Summarizer")
        window_size = self.config.get("window_size", {"width": 1000, "height": 800})
        window_min_size = self.config.get("window_min_size", {"width": 900, "height": 700})

        self.root.title(window_title)
        self.root.geometry(f"{window_size['width']}x{window_size['height']}")
        self.root.minsize(window_min_size["width"], window_min_size["height"])

        self.selected_file = ""
        self.summary_text = ""
        self.summary_length = tk.StringVar(value=self.config.get("default_summary", "medium"))
        self.status = tk.StringVar(value="Ready")
        self.progress_interval = self.config.get("progress_interval", 12)

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Local AI Text Summarizer",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=15)

        # -------------------------
        # Input Section
        # -------------------------
        input_frame = ttk.LabelFrame(
            self.root,
            text="Input Text",
            padding=10
        )
        input_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.input_box = tk.Text(
            input_frame,
            wrap="word",
            height=12,
            font=("Segoe UI", 11)
        )
        self.input_box.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # File Selection
        # -------------------------
        file_frame = ttk.Frame(self.root)
        file_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        ttk.Button(
            file_frame,
            text="Browse TXT File",
            command=self.browse_file
        ).pack(side="left")

        self.file_label = ttk.Label(
            file_frame,
            text="No file selected"
        )
        self.file_label.pack(
            side="left",
            padx=10
        )

        # -------------------------
        # Summary Length
        # -------------------------
        options = ttk.LabelFrame(
            self.root,
            text="Summary Length",
            padding=10
        )
        options.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ttk.Radiobutton(
            options,
            text="Short",
            variable=self.summary_length,
            value="short"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            options,
            text="Medium",
            variable=self.summary_length,
            value="medium"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            options,
            text="Long",
            variable=self.summary_length,
            value="long"
        ).pack(side="left", padx=10)

        # -------------------------
        # Buttons
        # -------------------------
        button_frame = ttk.Frame(self.root)
        button_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.generate_button = ttk.Button(
            button_frame,
            text="Generate Summary"
        )
        self.generate_button.pack(side="left")

        self.save_button = ttk.Button(
            button_frame,
            text="Save Summary as JSON",
            state="disabled"
        )
        self.save_button.pack(side="left", padx=10)

        self.processing_label = ttk.Label(
            self.root,
            text="Ready",
            font=("Segoe UI", 10)
        )
        self.processing_label.pack(fill="x", padx=15)

        self.progress = ttk.Progressbar(
            self.root,
            mode="indeterminate",
            orient="horizontal"
        )
        self.progress.pack(fill="x", padx=15, pady=5)

        # -------------------------
        # Statistics
        # -------------------------
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.original_words_label = ttk.Label(
            stats_frame,
            text="Original Words: 0"
        )
        self.original_words_label.pack(side="left")

        self.summary_words_label = ttk.Label(
            stats_frame,
            text="Summary Words: 0"
        )
        self.summary_words_label.pack(side="left", padx=30)

        self.time_taken_label = ttk.Label(
            stats_frame,
            text="Time Taken: 0.00 seconds"
        )
        self.time_taken_label.pack(side="left", padx=30)

        # -------------------------
        # Summary Output
        # -------------------------
        output_frame = ttk.LabelFrame(
            self.root,
            text="Generated Summary",
            padding=10
        )
        output_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        self.output_box = tk.Text(
            output_frame,
            wrap="word",
            height=10,
            font=("Segoe UI", 11),
            state="disabled"
        )
        self.output_box.pack(
            fill="both",
            expand=True
        )

        # -------------------------
        # Status Bar
        # -------------------------
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status,
            relief="sunken",
            anchor="w"
        )
        status_bar.pack(
            fill="x",
            side="bottom"
        )

        self.generate_button.configure(command=self.generate_summary)
        self.save_button.configure(command=self.save_json)

    # ==========================================
    # Browse TXT File
    # ==========================================
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select TXT File",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if not filename:
            return

        try:
            validate_file(filename)

            text = read_txt(filename)

            self.selected_file = filename
            self.file_label.config(text=filename)

            self.input_box.delete("1.0", tk.END)
            self.input_box.insert(tk.END, text)

            self.status.set("TXT file loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Failed to load file.")

    # ==========================================
    # Generate Summary
    # ==========================================
    def generate_summary(self):
        text = self.input_box.get("1.0", tk.END).strip()

        self.summary_text = ""
        self.generate_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.time_taken_label.config(text="Time Taken: 0.00 seconds")

        self.root.after(0, lambda: self.processing_label.config(text="⏳ Preparing summarization..."))
        self.root.after(0, lambda: self.status.set("Preparing summarization..."))
        self.root.after(0, lambda: self.progress.start(self.progress_interval))

        start_time = time.perf_counter()
        threading.Thread(
            target=self.run_summary,
            args=(text, start_time),
            daemon=True
        ).start()

    def run_summary(self, text, start_time):
        try:
            self.root.after(0, lambda: self.processing_label.config(text="✔ Validating input..."))
            self.root.after(0, lambda: self.status.set("Validating input..."))

            validate_text(text)
            cleaned_text = clean_text(text)

            self.root.after(0, lambda: self.processing_label.config(text="🤖 Loading AI model..."))
            self.root.after(0, lambda: self.status.set("Loading AI model..."))

            engine = TextSummarizer()

            self.root.after(0, lambda: self.processing_label.config(text="📝 Generating summary..."))
            self.root.after(0, lambda: self.status.set("Generating summary..."))

            summary = engine.summarize(
                cleaned_text,
                self.summary_length.get()
            )

            self.summary_text = summary
            original_words = word_count(cleaned_text)
            summary_words = word_count(summary)
            elapsed_time = time.perf_counter() - start_time

            self.root.after(
                0,
                lambda: self.update_summary_ui(
                    summary,
                    original_words,
                    summary_words,
                    elapsed_time
                )
            )
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def update_summary_ui(self, summary, original_words, summary_words, elapsed_time):
        self.progress.stop()

        self.processing_label.config(text="✅ Summary generated successfully!")

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, summary)
        self.output_box.config(state="disabled")

        self.original_words_label.config(text=f"Original Words: {original_words}")
        self.summary_words_label.config(text=f"Summary Words: {summary_words}")
        self.time_taken_label.config(text=f"Time Taken: {elapsed_time:.2f} seconds")

        self.generate_button.config(state="normal")
        self.save_button.config(state="normal")
        self.status.set("Summary generated successfully.")

    def show_error(self, message):
        self.progress.stop()

        self.processing_label.config(text="❌ Failed to generate summary.")
        self.generate_button.config(state="normal")
        self.save_button.config(state="disabled")
        self.status.set("Failed to generate summary.")

        messagebox.showerror("Error", message)

    # ==========================================
    # Save JSON
    # ==========================================
    def save_json(self):
        if not self.summary_text:
            messagebox.showwarning(
                "Warning",
                "Generate a summary first."
            )
            return

        try:
            filename = filedialog.asksaveasfilename(
                title="Save Summary",
                defaultextension=".json",
                filetypes=[
                    ("JSON Files", "*.json")
                ]
            )

            if not filename:
                return

            import json
            from datetime import datetime

            original_text = self.input_box.get(
                "1.0",
                tk.END
            ).strip()

            data = {
                "summary_type": self.summary_length.get(),
                "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "original_word_count": word_count(original_text),
                "summary_word_count": word_count(self.summary_text),
                "summary": self.summary_text,
                "original_text": original_text
            }

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    data,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            self.status.set("Summary saved successfully.")
            messagebox.showinfo("Success", "Summary saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ==========================================
# Start Application
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()