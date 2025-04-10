import sys
import os
import site
from cx_Freeze import setup, Executable

# Add Tkinter data files (needed for themed widgets)
def find_tkinter_data_files():
    tkinter_data = []
    tcl_dir = ''
    
    # Look for TCL/TK data files in standard locations
    if sys.platform == "win32":
        for path in site.getsitepackages():
            tcl_path = os.path.join(path, 'tcl')
            if os.path.exists(tcl_path):
                for dirpath, _, filenames in os.walk(tcl_path):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        rel_path = os.path.relpath(file_path, tcl_path)
                        tkinter_data.append((os.path.join("lib", "tcl", os.path.dirname(rel_path)), [file_path]))
    
    return tkinter_data

# Get Tkinter data files
tk_data_files = find_tkinter_data_files()

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": [
        "os", 
        "tkinter", 
        "pandas", 
        "pdfplumber", 
        "re", 
        "sqlite3", 
        "typing", 
        "PIL", 
        "cryptography",
        "PyPDF2",
        "reportlab"
    ],
    "excludes": ["test", "distutils", "unittest", "PyQt6"],  # Exclude PyQt6
=======
    "excludes": ["test", "distutils", "unittest"],
        "os", 
        "tkinter", 
        "pandas", 
        "pdfplumber", 
        "re", 
        "sqlite3", 
        "typing", 
        "PIL", 
        "cryptography",
        "PyPDF2",
        "reportlab"
    ],
    "excludes": ["test", "distutils", "unittest"],
    "include_files": [
        # Include all Python files
        ("alin1.py", "alin1.py"),
        ("db_handler.py", "db_handler.py"),
        ("tddim.py", "tddim.py"),
        ("tddm.py", "tddm.py"),
        ("tdmplm.py", "tdmplm.py"),
        ("tdmplmd.py", "tdmplmd.py"),
        ("ensure_directories.py", "ensure_directories.py"),
        ("README.md", "README.md"),
        ("PostInstallationGuide.txt", "PostInstallationGuide.txt"),
        # Create empty data directory structure
        ("data/", "data/"),
        # Include input data directory
        ("data/input/", "data/input/"),
    ],
    "include_msvcr": True,
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
    "build_exe": "build/PDFProcessor",
}

# Add Tkinter data files to the build options
build_exe_options["include_files"].extend(tk_data_files)

# Base configurations
console_base = None  # Used for any console utilities
# Win32GUI base hides console window for GUI applications
gui_base = "Win32GUI" if sys.platform == "win32" else None

# Define our icon file - create a default if we don't have one
icon_file = None
if os.path.exists("app_icon.ico"):
    icon_file = "app_icon.ico"

# Create a list of all executables
executables = [
    # Main application with GUI base (no console)
    Executable(
        "alin1.py",
        base=gui_base,
        target_name="PDFProcessor.exe",
        icon=icon_file,
        shortcut_name="PDF Processor",
        shortcut_dir="DesktopFolder",
    ),
    # Module executables
    Executable(
        "tddm.py",
        base=gui_base,
        target_name="tddm.exe",
        icon=icon_file,
    ),
    Executable(
        "tddim.py",
        base=gui_base,
        target_name="tddim.exe",
        icon=icon_file,
    ),
    Executable(
        "tdmplm.py",
        base=gui_base,
        target_name="tdmplm.exe",
        icon=icon_file,
    ),
    Executable(
        "tdmplmd.py",
        base=gui_base,
        target_name="tdmplmd.exe",
        icon=icon_file,
    ),
]

# MSI Installer options
bdist_msi_options = {
    "upgrade_code": "{518CEA60-2795-4950-A282-91F6EC6B0A11}",  # Unique identifier for the app
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\PDF Processor",
    "install_icon": icon_file,
}

setup(
    name="PDF Processing Tool",
    version="1.0.0",
    description="PDF Processing Application for Task, Description, and Documentation",
    author="",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=executables,
)
