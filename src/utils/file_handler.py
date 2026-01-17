import json
import os
import yaml

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def save_json(data, output_path):
    """Saves dictionary data to a JSON file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def list_files(directory, extensions=[".jpg", ".png", ".jpeg", ".pdf"]):
    """Generator to list valid images in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                yield os.path.join(root, file)