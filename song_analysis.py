from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime
import os
import json

output_file_path = 'bird_data/SGL300-2_2021.json'

def append_to_output_file(new_data, file_path):
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(new_data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=2)

directory = 'song_files/SGL300_2021/ARU2'

for filename in os.listdir(directory):
    if filename.endswith('.WAV'):
        file_path = os.path.join(directory, filename)
        print(file_path)

        analyzer = Analyzer()

        recording = Recording(
            analyzer,
            file_path,
            date=datetime(year=2022, month=5, day=10),  # use date or week_48
            min_conf=0.75,
        )
        recording.analyze()
        detections = recording.detections

        # Extract relevant information from detections if needed
        output_data = [{'common_name': detection['common_name'],
                        'scientific_name': detection['scientific_name'],
                        'start_time': detection['start_time'],
                        'end_time': detection['end_time'],
                        'confidence': detection['confidence'],
                        'label': detection['label'], 
                        'recording name': filename} for detection in detections]

        # Append data to the output file
        append_to_output_file(output_data, output_file_path)
