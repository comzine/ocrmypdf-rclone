import json
import time
import logging
from pathlib import Path
import ocrmypdf

print("started watchit.py")

# Set the path to your JSON settings file
json_settings_path = '/ocrmypdf.json'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='ocrmypdf_watcher.log',
    filemode='a'
)

# Load JSON settings
def load_json_settings(settings_path):
    with open(settings_path, 'r') as settings_file:
        return json.load(settings_file)

ocr_settings = load_json_settings(json_settings_path)

# Process a single PDF using OCR settings
def process_pdf(input_path, output_path):
    logging.info(f"Processing file: {input_path}")
    try:
        # Prepare language settings
        languages = ocr_settings.get("l", "eng").split('+')

        # Call the OCR function with settings from JSON
        result = ocrmypdf.ocr(
            input_file=input_path,
            output_file=output_path,
            rotate_pages=ocr_settings.get("rotate_pages", False),
            language=languages,
            clean=ocr_settings.get("clean", False)
        )
        # Handle the result
        if result == ocrmypdf.ExitCode.ok:
            input_path.unlink()
            logging.info("OCR complete")
        elif result == ocrmypdf.ExitCode.already_done_ocr:
            logging.info("Skipped document because it already contained text")
        else:
            logging.warning(f"OCR did not complete for {input_path}. Result: {result}")
    except Exception as e:
        logging.error(f"An error occurred while processing {input_path}: {e}")

# Watch a folder and process any PDF files
def watch_folder(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    processed_files = set()

    for file_path in sorted(input_path.glob('**/*.pdf')):
        if file_path.name not in processed_files:
            output_file_path = output_path / file_path.name
            process_pdf(file_path, output_file_path)
            processed_files.add(file_path.name)
            # Wait until the file is removed (if set to do so) or timeout after 5 minutes
            start_time = time.time()
            while file_path.exists():
                if time.time() - start_time > 300:  # 5 minutes
                    logging.error(f"Timeout: Processing of file {file_path} took longer than 5 minutes.")
                    break
                time.sleep(1)

if __name__ == '__main__':
    # Define your input and output folders
    input_folder = '/input'  # Replace with your input folder path
    output_folder = '/output'  # Replace with your output folder path

    # Process existing files on startup
    watch_folder(input_folder, output_folder)
    # Start the watching loop
    while True:
        watch_folder(input_folder, output_folder)
        time.sleep(10)  # Check every 10 seconds for new files

