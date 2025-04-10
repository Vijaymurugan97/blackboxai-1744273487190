# PDF Processor Application

A specialized application for processing and extracting data from PDF files with various formats and structures. This tool supports different parsing methods for specific document types related to tasks, descriptions, documentation, intervals, margins, and part numbers.

## Features

- Extract structured data from PDF documents
- Process various PDF formats through specialized modules
- Edit extracted data in a user-friendly interface
- Export data to Excel format
- Store processed data in a local database

## Installation

### Using the Windows Installer

1. Download the installer (.msi file) from the releases section
2. Run the installer and follow the on-screen instructions
3. Once installed, launch "PDF Processor" from your desktop or start menu

### Building from Source

If you prefer to build the installer yourself:

1. Ensure you have Python 3.7 or higher installed
2. Clone or download this repository
3. Run the `build_installer.bat` file
4. The installer will be created in the `dist` folder

## Usage

1. Launch the application
2. From the main interface, select the appropriate converter based on your PDF format:
   - Task/Description/Documentation/Margin (TDDM)
   - Task/Description/Documentation/Interval/Margin (TDDIM)
   - Task/Description/MP/N/PN/Limit/Margin (TDMPLM)
   - Task/Description/MP/N/PN/Limit/Margin/Documentation (TDMPLMD)
3. In the converter interface, click "Browse" to select your PDF file
4. Click "Process PDF" to extract the data
5. Edit the extracted data as needed by double-clicking on cells
6. Export the processed data to Excel using the "Export to Excel" button

## Data Storage

The application stores processed data in a SQLite database located in the `data` folder. Input PDFs can be stored in the `data/input` directory for convenient access.

## System Requirements

- Windows 7 or higher
- 4GB RAM (recommended)
- 200MB free disk space
