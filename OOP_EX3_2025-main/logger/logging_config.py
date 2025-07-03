import logging
import os

# Determine the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure the log directory exists
log_directory = os.path.join(project_root, 'logger')
os.makedirs(log_directory, exist_ok=True)

# Configure logging to include only the message
log_file = os.path.join(log_directory, 'library.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')

# Create a logger object
logger = logging.getLogger('library_logger')