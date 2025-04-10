import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import pdfplumber
import re
import os
from typing import List, Dict,Tuple, Any
from db_handler import Database

class PDFProcessor:
    def __init__(self, db: Database):
        self.db = db
        self.columns = ["ATA", "Task Number", "Description", "Documentation",  "Margin", "Reference"]
        
        # Common patterns
        self.known_refs  = [
            (r'[A-Z]{3}\s*\d{2}\s*.\s*\d{2}\s*.\s*\d{2}\s*.\s*\d{3}\b',lambda m: re.sub(r'\s+', '', m.group(0))),
            (r'[A-Z]{3}\s*\d{2}\s*.\s*\d{2}\s*.\s*\d{2}\b',lambda m: re.sub(r'\s+', '', m.group(0)))
        ]
        
        # Known good values for pattern matching
        self.known_doc = { "MET 21.51.10.601","CMM 25.69.87"}


    def main():
        print("Executing tddm.py script!")
    if __name__ == "__main__":
        main()
        
    
    def extract_ata(self, text: str) -> str:
        match = re.search(r"\b(\d{2})/(\d{2})/\d{2}/\d{3}/\d{3}/\d{3}\b", text)
        if match:
            return f"{match.group(1)}-{match.group(2)}"
        match = re.search(r"ATA\s+(\d{2})\s*[-\s]\s*(\d{2})", text)
        if match:
            return f"{match.group(1)}-{match.group(2)}"
        return ""
    
    def extract_task_number(self, text: str) -> str:
        match = re.search(r"\b(\d{2}/\d{2}/\d{2}/\d{3}/\d{3}/\d{3})\b", text)
        return match.group(0) if match else ""

    def extract_description(self, text: str) -> str:
        # First try to find description after task number
        task_match = re.search(r"\b\d{2}/\d{2}/\d{2}/\d{3}/\d{3}/\d{3}\b\s*(.*?)(?=ALL\s+MP/N|\d{6}|\d{3}[A-Z]|\b\d+\s*[MF]H|\bMET|\bMET|$)", text)
        if task_match:
            desc = task_match.group(1).strip()
            # Clean up description
            desc = re.sub(r'\([^)]*\)', '', desc)  # Remove parenthetical content
            desc = re.sub(r'\s+', ' ', desc)  # Normalize whitespace
            desc = re.sub(r'^\s*-\s*', '', desc)  # Remove leading dash
            desc = desc.strip()
            if desc:
                return desc
        
        # Fallback to line-by-line search
        lines = text.split('\n')
        for line in lines:
            # Skip task numbers and part numbers
            if re.search(r'\b\d{2}/\d{2}/\d{2}/\d{3}/\d{3}/\d{3}\b', line):
                continue
            if re.search(r'\bALL\s+MP/N\b|\b\d{6}\b|\b\d{3}[A-Z]', line):
                continue
            if re.search(r'\b\d+\s*[MF]H\b|\bTSM\b|\bTSI\b', line):
                continue
            
            # Clean up line
            line = re.sub(r'\([^)]*\)', '', line)  # Remove parenthetical content
            line = re.sub(r'\s+', ' ', line)  # Normalize whitespace
            line = re.sub(r'^\s*-\s*', '', line)  # Remove leading dash
            line = line.strip()
            
            if line:
                return line
        
        return "-"

    def extract_documentation(self, text: str) -> List[str]:
        ref_matches = set()

        # Look for "MET XX.XX.XX.XXX" or "CMM XX.XX.XX" patterns
        for match in re.finditer(r"\b(CMM\s+\d{2}\.\d{2}\.\d{2}|MET\s+\d{2}\.\d{2}\.\d{2}\.\d{3})\b", text):
            ref = match.group(1).strip()

            # Check if similar to known references
            if ref not in self.known_refs:
                for known_ref in self.known_refs:
                    if ref in self.known_doc:
                        ref = known_ref
                        break

            self.known_refs.append(ref)
            ref_matches.add(ref)

        return list(ref_matches)  # Return unique matches


    def process_pdf(self, pdf_path: str) -> pd.DataFrame:
        structured_data = {col: [] for col in self.columns}
        all_refs = set()  # ✅ Collect all unique documentation references

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                lines = text.split('\n')
                for i, line in enumerate(lines):
                    task_number = self.extract_task_number(line)
                    if task_number:
                        context = " ".join(lines[i:i+3])
                        desc = self.extract_description(context)
                        documentation_refs = self.extract_documentation(context)
                        ata = self.extract_ata(line)

                        for doc in documentation_refs:
                            if doc not in all_refs:
                                print("Extracted:", doc)
                                all_refs.add(doc)

                            structured_data["ATA"].append(ata)
                            structured_data["Task Number"].append(task_number)
                            structured_data["Description"].append(desc)
                            structured_data["Documentation"].append(doc)
                            structured_data["Margin"].append("0")
                            structured_data["Reference"].append(context)

        df = pd.DataFrame(structured_data)
        self.db.save_processed_data(df)
        return df

class EditableTreeview(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Double-1>', self.on_double_click)
        self.entry = None
        self.current_item = None
        self.current_column = None
    
    def on_double_click(self, event):
        region = self.identify_region(event.x, event.y)
        if region != "cell":
            return
        
        column = self.identify_column(event.x)
        item = self.identify_row(event.y)
        
        if not column or not item:
            return
        
        column_name = self["columns"][int(column[1]) - 1]
        x, y, w, h = self.bbox(item, column)
        
        self.entry = ttk.Entry(self, width=w//8)
        self.entry.place(x=x, y=y, width=w, height=h)
        
        value = self.item(item)['values'][int(column[1]) - 1]
        self.entry.insert(0, value)
        self.entry.select_range(0, tk.END)
        self.entry.focus()
        
        self.current_item = item
        self.current_column = int(column[1]) - 1
        
        self.entry.bind('<Return>', self.on_entry_return)
        self.entry.bind('<Escape>', lambda e: self.entry.destroy())
        self.entry.bind('<FocusOut>', self.on_focus_out)
    
    def on_entry_return(self, event):
        self.save_edit()
    
    def on_focus_out(self, event):
        self.save_edit()
    
    def save_edit(self):
        if not self.entry:
            return
        
        value = self.entry.get()
        if 3 <= len(value) <= 15:
            values = list(self.item(self.current_item)['values'])
            values[self.current_column] = value
            self.item(self.current_item, values=values)
            
            # Save to database
            try: 
                data = {col: val for col, val in zip(self["columns"], values)}
                self.master.master.master.db.save_processed_data(pd.DataFrame([data]))
            except Exception as e:
                print(f"Error saving to database: {e}")
        else:
            messagebox.showwarning("Invalid Input", 
                "Please enter between 3 and 15 characters.")
        
        self.entry.destroy()
        self.entry = None

class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("tddm Converter")
        self.current_df = None
        
        try:
            self.db = Database()
            self.processor = PDFProcessor(self.db)
        except Exception as e:
            messagebox.showerror("Error", f"Error initializing database: {str(e)}")
            self.db = None
            self.processor = None
        
        self.setup_ui()

    def main(self):
        print("Executing tddm.py script!")
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for file selection
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Open DMCs Folder", 
                  command=self.browse_dmcs_folder).pack(side=tk.LEFT)
        ttk.Label(file_frame, text="  |  ").pack(side=tk.LEFT)
        
        ttk.Label(file_frame, text="Select PDF File:").pack(side=tk.LEFT)
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, 
                 width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Browse", 
                  command=self.browse_file).pack(side=tk.LEFT)
        ttk.Button(file_frame, text="Process PDF", 
                  command=self.process_file).pack(side=tk.LEFT, padx=5)
        
        # Preview frame
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        self.tree = EditableTreeview(preview_frame)
        
        # Scrollbars
        vsb = ttk.Scrollbar(preview_frame, orient="vertical", 
                           command=self.tree.yview)
        hsb = ttk.Scrollbar(preview_frame, orient="horizontal", 
                           command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        # Bottom frame
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(bottom_frame, text="Export to Excel", 
                  command=self.export_excel).pack(side=tk.RIGHT)
    
    def browse_dmcs_folder(self):
        dmcs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "input")
        if not os.path.exists(dmcs_path):
            os.makedirs(dmcs_path)
        
        file_path = filedialog.askopenfilename(
            initialdir=dmcs_path,
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def process_file(self):
        if not self.processor:
            messagebox.showerror("Error", "Database not initialized")
            return
        
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a PDF file first")
            return
        
        try:
            self.current_df = self.processor.process_pdf(file_path)
            self.update_preview()
            messagebox.showinfo("Success", "PDF processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error processing PDF: {str(e)}")
    
    def update_preview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree["columns"] = list(self.current_df.columns)
        self.tree["show"] = "headings"
        
        for column in self.current_df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)
        
        for _, row in self.current_df.iterrows():
            self.tree.insert("", "end", values=list(row))
    
    def export_excel(self):
        if self.current_df is None:
            messagebox.showerror("Error", "No data to export. Please process a PDF first.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                self.current_df.to_excel(file_path, index=False, sheet_name='Extracted Data')
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting to Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
    c=PDFProcessor()
    c.main()