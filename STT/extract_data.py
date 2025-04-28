#add parent directory as an import path
import sys
from os.path import dirname, abspath
parentDir = dirname(dirname(abspath(__file__)))
sys.path.insert(1, parentDir)
from config import LOG_FOLDER
import json

def extract_user_text(file_path=f'STT/{LOG_FOLDER}/app.json'):
    try:
        user_texts = []
        with open(file_path, 'r') as file:
            data = json.load(file)

            for entry in data:
                user_texts.append(entry['text']['text'])

        return user_texts
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

if __name__ == "__main__":
    results = extract_user_text()
    # Testing
    for text in results:
        print(text)
