import os
import sys

def ensure_app_directories():
    """
    Ensures that all required application directories exist.
    Creates them if they don't exist.
    """
    # Get the application's root directory
    if getattr(sys, 'frozen', False):
        # We are running in a bundle
        app_dir = os.path.dirname(sys.executable)
    else:
        # We are running in a normal Python environment
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define required directories
    data_dir = os.path.join(app_dir, "data")
    input_dir = os.path.join(data_dir, "input")
    
    # Create directories if they don't exist
    for directory in [data_dir, input_dir]:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Error creating directory {directory}: {str(e)}")
    
    return data_dir, input_dir

if __name__ == "__main__":
    # Test the function if this script is run directly
    data_dir, input_dir = ensure_app_directories()
    print(f"Data directory: {data_dir}")
    print(f"Input directory: {input_dir}")
