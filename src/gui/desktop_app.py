#!/usr/bin/env python3
"""
Desktop GUI for Model-to-Code Generator using tkinter
Provides a native desktop interface for model conversion
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.parsers.text_parser import TextModelParser
from src.generators.python_generator import PythonCodeGenerator
from src.generators.java_generator import JavaCodeGenerator
from src.generators.typescript_generator import TypeScriptCodeGenerator


class ModelToCodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Model-to-Code Generator")
        self.root.geometry("1200x800")
        
        # Initialize generators
        self.generators = {
            'Python': PythonCodeGenerator(),
            'Java': JavaCodeGenerator(),
            'TypeScript': TypeScriptCodeGenerator()
        }
        
        self.parser = TextModelParser()
        self.current_files = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Model-to-Code Generator", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Input
        input_frame = ttk.LabelFrame(main_frame, text="Model Input", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(2, weight=1)
        
        # File selection
        file_frame = ttk.Frame(input_frame)
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Input File:").grid(row=0, column=0, sticky=tk.W)
        self.file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_var)
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=2)
        
        # Format selection
        format_frame = ttk.Frame(input_frame)
        format_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(format_frame, text="Format:").grid(row=0, column=0, sticky=tk.W)
        self.format_var = tk.StringVar(value="Simple Text")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var,
                                   values=["Simple Text", "PlantUML", "YAML"], state="readonly")
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # Model text input
        ttk.Label(input_frame, text="Model Text:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        self.text_input = scrolledtext.ScrolledText(input_frame, width=50, height=20, font=('Consolas', 10))
        self.text_input.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Right panel - Output
        output_frame = ttk.LabelFrame(main_frame, text="Generated Code", padding="10")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(2, weight=1)
        
        # Language selection and buttons
        controls_frame = ttk.Frame(output_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        controls_frame.columnconfigure(2, weight=1)
        
        ttk.Label(controls_frame, text="Language:").grid(row=0, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="Python")
        language_combo = ttk.Combobox(controls_frame, textvariable=self.language_var,
                                     values=["Python", "Java", "TypeScript"], state="readonly")
        language_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 10))
        
        ttk.Button(controls_frame, text="Generate Code", command=self.generate_code).grid(row=0, column=3, padx=(5, 0))
        ttk.Button(controls_frame, text="Save All", command=self.save_files).grid(row=0, column=4, padx=(5, 0))
        
        # File tabs
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Sample data button
        sample_frame = ttk.Frame(input_frame)
        sample_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Button(sample_frame, text="Load Sample", command=self.load_sample).grid(row=0, column=0)
        ttk.Button(sample_frame, text="Clear", command=self.clear_input).grid(row=0, column=1, padx=(5, 0))
    
    def browse_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[
                ("Text files", "*.txt"),
                ("PlantUML files", "*.puml *.plantuml"),
                ("YAML files", "*.yaml *.yml"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.file_var.set(filename)
            
            # Auto-detect format
            ext = Path(filename).suffix.lower()
            if ext in ['.puml', '.plantuml']:
                self.format_var.set("PlantUML")
            elif ext in ['.yaml', '.yml']:
                self.format_var.set("YAML")
            else:
                self.format_var.set("Simple Text")
            
            # Load file content
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, content)
                self.status_var.set(f"Loaded: {Path(filename).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def load_sample(self):
        """Load sample model"""
        sample_models = {
            "Simple Text": """User:
  id: int
  username: string
  email: string
  getId()
  setUsername(name: string)
  validateEmail()

Product:
  id: int
  name: string
  price: float
  getName()
  setPrice(price: float)""",
            
            "PlantUML": """@startuml
class User {
    - id: int
    - username: string
    - email: string
    + getId(): int
    + setUsername(name: string): void
    + validateEmail(): boolean
}

class Product {
    - id: int
    - name: string
    - price: float
    + getName(): string
    + setPrice(price: float): void
}

User --> Product : "purchases"
@enduml""",
            
            "YAML": """name: "Sample System"
classes:
  - name: User
    attributes:
      - name: id
        type: int
        visibility: private
      - name: username
        type: string
        visibility: private
    methods:
      - name: getId
        return_type: int
        visibility: public"""
        }
        
        format_key = self.format_var.get()
        sample_text = sample_models.get(format_key, sample_models["Simple Text"])
        
        self.text_input.delete(1.0, tk.END)
        self.text_input.insert(1.0, sample_text)
        self.status_var.set("Sample model loaded")
    
    def clear_input(self):
        """Clear input text"""
        self.text_input.delete(1.0, tk.END)
        self.file_var.set("")
        self.status_var.set("Input cleared")
    
    def generate_code(self):
        """Generate code from model"""
        model_text = self.text_input.get(1.0, tk.END).strip()
        
        if not model_text:
            messagebox.showwarning("Warning", "Please enter a model or load a file")
            return
        
        try:
            self.status_var.set("Parsing model...")
            self.root.update()
            
            # Parse model
            format_map = {
                "Simple Text": "simple",
                "PlantUML": "plantuml", 
                "YAML": "yaml"
            }
            
            format_key = format_map[self.format_var.get()]
            
            if format_key == "plantuml":
                diagram = self.parser.parse_plantuml(model_text)
            elif format_key == "yaml":
                diagram = self.parser.parse_yaml(model_text)
            else:
                diagram = self.parser.parse_simple_text(model_text)
            
            self.status_var.set("Generating code...")
            self.root.update()
            
            # Generate code
            language = self.language_var.get()
            generator = self.generators[language]
            generated_files = generator.generate(diagram)
            
            self.current_files = generated_files
            self.display_generated_files()
            
            self.status_var.set(f"Generated {len(generated_files)} files successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate code: {e}")
            self.status_var.set("Generation failed")
    
    def display_generated_files(self):
        """Display generated files in tabs"""
        # Clear existing tabs
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        
        # Create tabs for each file
        for filename, content in self.current_files.items():
            frame = ttk.Frame(self.notebook)
            
            # Add copy button
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Button(btn_frame, text=f"Copy {filename}", 
                      command=lambda f=filename: self.copy_to_clipboard(f)).pack(side=tk.RIGHT)
            
            # Add text widget with content
            text_widget = scrolledtext.ScrolledText(frame, font=('Consolas', 10))
            text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            text_widget.insert(1.0, content)
            text_widget.config(state=tk.DISABLED)  # Read-only
            
            self.notebook.add(frame, text=filename)
    
    def copy_to_clipboard(self, filename):
        """Copy file content to clipboard"""
        content = self.current_files.get(filename, "")
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_var.set(f"Copied {filename} to clipboard")
    
    def save_files(self):
        """Save all generated files"""
        if not self.current_files:
            messagebox.showwarning("Warning", "No files to save. Generate code first.")
            return
        
        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
        
        try:
            output_path = Path(output_dir)
            saved_count = 0
            
            for filename, content in self.current_files.items():
                file_path = output_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_count += 1
            
            self.status_var.set(f"Saved {saved_count} files to {output_dir}")
            messagebox.showinfo("Success", f"Saved {saved_count} files to {output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save files: {e}")


def main():
    root = tk.Tk()
    app = ModelToCodeGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()