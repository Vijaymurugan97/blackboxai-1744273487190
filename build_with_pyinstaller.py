"""
Script to build executable files using PyInstaller
"""
import os
import subprocess
import sys

def ensure_pyinstaller():
    """Ensure PyInstaller is installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")

def build_main_executable():
    """Build the main application executable"""
    print("Building main application executable...")
    cmd = [
        "pyinstaller",
        "--name=PDFProcessor",
        "--windowed",  # No console window for GUI app
        "--add-data=README.md:.",
        "--add-data=PostInstallationGuide.txt:.",
        "--hidden-import=pandas",
        "--hidden-import=pdfplumber",
        "alin1.py"
    ]
    subprocess.check_call(cmd)
    
    # Create required directories
    try:
        os.makedirs("dist/PDFProcessor/data/input", exist_ok=True)
        print("Created data directories in output folder.")
    except Exception as e:
        print(f"Error creating directories: {e}")

def build_module_executables():
    """Build executables for each module"""
    modules = ["tddm.py", "tddim.py", "tdmplm.py", "tdmplmd.py"]
    
    for module in modules:
        module_name = os.path.splitext(module)[0]
        print(f"Building {module_name} executable...")
        cmd = [
            "pyinstaller",
            f"--name={module_name}",
            "--windowed",  # No console window for GUI app
            "--hidden-import=pandas",
            "--hidden-import=pdfplumber",
            module
        ]
        subprocess.check_call(cmd)
        
        # Copy module executable to main folder
        src_folder = f"dist/{module_name}"
        dest_folder = "dist/PDFProcessor"
        
        if os.path.exists(src_folder):
            for item in os.listdir(src_folder):
                src_item = os.path.join(src_folder, item)
                dest_item = os.path.join(dest_folder, item)
                
                if not os.path.exists(dest_item):
                    if os.path.isdir(src_item):
                        os.makedirs(dest_item, exist_ok=True)
                        for subitem in os.listdir(src_item):
                            src_subitem = os.path.join(src_item, subitem)
                            dest_subitem = os.path.join(dest_item, subitem)
                            if not os.path.exists(dest_subitem):
                                if os.path.isfile(src_subitem):
                                    with open(src_subitem, 'rb') as f_src:
                                        with open(dest_subitem, 'wb') as f_dest:
                                            f_dest.write(f_src.read())
                    elif os.path.isfile(src_item):
                        with open(src_item, 'rb') as f_src:
                            with open(dest_item, 'wb') as f_dest:
                                f_dest.write(f_src.read())

def main():
    # Ensure PyInstaller is installed
    ensure_pyinstaller()
    
    # Build main executable
    build_main_executable()
    
    # Build module executables
    build_module_executables()
    
    print("\nBuild complete! Executables are in the 'dist/PDFProcessor' folder.")

if __name__ == "__main__":
    main()
