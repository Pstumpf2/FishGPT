#add parent directory as an import path
import sys
from os import path, makedirs
parentDir = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.insert(1, parentDir)
from config import LOG_FOLDER

import datetime as dt
import inspect
import json
# The format in which the date and time will appear with on the log file
datetime_format = '%m-%d-%Y %H:%M:%S'
# The designated path to the log file
log_file_path = f'STT/{LOG_FOLDER}/app.json'

# Ensure the 'Output' directory exists
if not path.exists(f'STT/{LOG_FOLDER}'):
    # if not, creates it
    makedirs(f'STT/{LOG_FOLDER}')

# Logs various program actions in the 'Output/app.log' file
def log_message(message, linenumber=False):
    line_number = -1
    if linenumber:
        # Get the current frame
        current_frame = inspect.currentframe()
        # Get the called frame
        caller_frame = current_frame.f_back
        # Get the line number from the caller frame
        line_number = caller_frame.f_lineno

    # Get the timestamp
    timestamp = dt.datetime.now().strftime(datetime_format)

    # Create a structured log entry
    log_entry = {
        "timestamp": timestamp,
        "text": message
    }

    if line_number != -1:
        log_entry["line_number"] = line_number

    try:
        # Read existing data or initialize an empty list
        if path.exists(log_file_path) and path.getsize(log_file_path) > 0:
            with open(log_file_path, 'r') as log_file:
                try:
                    logs = json.load(log_file)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        # Append the new entry and write back
        logs.append(log_entry)
        with open(log_file_path, 'w') as log_file:
            json.dump(logs, log_file, indent=1)
    except Exception as e:
        print(f'Failed to log message: {str(e)}')
