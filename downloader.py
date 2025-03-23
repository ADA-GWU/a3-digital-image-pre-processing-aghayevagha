import os
import requests

# Dynamically get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "E1154S7I.dcm")

url = "https://physionet.org/content/images/1.0.0/E1154S7I.dcm"

try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f" File downloaded successfully to {output_path}")
except requests.exceptions.RequestException as e:
    print(f" Failed to download file: {e}")
