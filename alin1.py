import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import sys
from typing import List, Dict, Any
from db_handler import Database
import subprocess
from ensure_directories import ensure_app_directories

# Ensure all required directories exist
ensure_app_directories()

class PDFProcessor:
    def __init__(self, db: Database):
        self.db = db
        
        self.columns_tdmplm=["ATA", "Task Number", "Description", "MP/N", "PN", "Limit", "Margin", "Reference"]
        self.columns_tddm = ["ATA", "Task Number", "Description", "Documentation",  "Margin", "Reference"]
        self.columns_tdmplmd = ["ATA", "Task Number", "Description", "MP/N", "PN", "Limit", "Margin","Documentation", "Reference"]
        self.columns_tddim = ["ATA", "Task Number", "Description", "Documentation","Interval",  "Margin", "Reference"]

        



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
        self.root.title("PDF to Excel Converter")
        self.current_df = None
        
        try:
            self.db = Database()
            self.processor = PDFProcessor(self.db)
        except Exception as e:
            messagebox.showerror("Error", f"Error initializing database: {str(e)}")
            self.db = None
            self.processor = None
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        label = ttk.Label(file_frame, text="Choose the respective file format", 
                  font=("Arial", 12, "bold"), foreground="#3C75A0")
        label.pack(pady=5)
                   
        ttk.Button(file_frame, text=["Task","/","Description","/","Documentation","/","Margin"] ,
                  command=self.tddm).pack(fill=tk.X, pady=2)
        
        ttk.Button(file_frame, text=["Task","/","Description","/","Documentation","/","Interval","/","Margin"] ,
                  command=self.tddim).pack(fill=tk.X, pady=2)
        
        ttk.Button(file_frame, text=["Task","/","Description","/","MP/N","/","PN","/","Limit","/","Margin"] ,
                  command=self.tdmplm).pack(fill=tk.X, pady=2)
        
        ttk.Button(file_frame, text=["Task","/","Description","/","MP/N","/","PN","/","Limit","/","Margin","/","Documentation"] ,
                  command=self.tdmplmd).pack(fill=tk.X, pady=2)

    def tddm(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
            if sys.platform == 'win32':
                subprocess.run([os.path.join(script_dir, "tddm.exe")])
            else:
                subprocess.run([os.path.join(script_dir, "tddm")])
        else:
            # Running in development environment
            subprocess.run([sys.executable, "tddm.py"])
        print("Executing tddm script!")

    def tddim(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
            if sys.platform == 'win32':
                subprocess.run([os.path.join(script_dir, "tddim.exe")])
            else:
                subprocess.run([os.path.join(script_dir, "tddim")])
        else:
            # Running in development environment
            subprocess.run([sys.executable, "tddim.py"])
        print("Executing tddim script!")

    def tdmplm(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
            if sys.platform == 'win32':
                subprocess.run([os.path.join(script_dir, "tdmplm.exe")])
            else:
                subprocess.run([os.path.join(script_dir, "tdmplm")])
        else:
            # Running in development environment
            subprocess.run([sys.executable, "tdmplm.py"])
        print("Executing tdmplm script!")

    def tdmplmd(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = os.path.dirname(sys.executable)
            if sys.platform == 'win32':
                subprocess.run([os.path.join(script_dir, "tdmplmd.exe")])
            else:
                subprocess.run([os.path.join(script_dir, "tdmplmd")])
        else:
            # Running in development environment
            subprocess.run([sys.executable, "tdmplmd.py"])
        print("Executing tdmplmd script!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
    
