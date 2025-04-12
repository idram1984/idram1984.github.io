import subprocess
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"book_update_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_command(command, cwd=None):
    """Run a command and log its output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        logging.info(f"Command {' '.join(command)} executed successfully")
        if result.stdout:
            logging.info(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {' '.join(command)}")
        logging.error(f"Error: {e.stderr}")
        return False

def update_book():
    logging.info("Starting book update process")
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    docs_dir = project_root / "docs"
    notebooks_dir = docs_dir / "notebooks"
    
    # Run your data collection notebooks
    logging.info("Executing notebooks...")
    for notebook in notebooks_dir.glob("*.ipynb"):
        logging.info(f"Processing {notebook.name}...")
        if not run_command([
            "poetry", "run", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            str(notebook)
        ], cwd=project_root):
            logging.error(f"Failed to execute {notebook.name}")
            return False
    
    # Build the book
    logging.info("Building the book...")
    if not run_command([
        "poetry", "run", "jupyter-book", "build", "docs"
    ], cwd=project_root):
        logging.error("Failed to build the book")
        return False
    
    logging.info(f"Book update completed successfully at {datetime.now()}")
    return True

if __name__ == "__main__":
    try:
        success = update_book()
        sys.exit(0 if success else 1)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1) 