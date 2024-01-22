"""
This is useful to generate json data files by reading the data file as csv.
"""

import csv
import json
import os
import sys
from collections import defaultdict

def parse_header(header):
    """ Parse the header to get the filename and the JSON key. """
    parts = header.split('.')
    return parts[0], '.'.join(parts[1:]) if len(parts) > 1 else None

def set_value(dct, keys, value):
    """ Set a value in a nested dictionary based on a list of keys. """
    for key in keys[:-1]:
        if key not in dct or not isinstance(dct[key], dict):
            dct[key] = {}
        dct = dct[key]
    dct[keys[-1]] = value if value != '' else None

def write_json_files(data, written_files, output_dir):
    """ Write the organized data to JSON files, each JSON object in a single line. """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename, contents in data.items():
        file_path = os.path.join(output_dir, f"{filename}.json")
        mode = 'a' if filename in written_files else 'w'
        with open(file_path, mode, encoding='utf-8') as json_file:
            for content in contents:
                json.dump(content, json_file)
                json_file.write('\n')
        written_files.add(filename)

def csv_to_json(csv_file_paths, output_dir):
    written_files = set()
    for csv_file_path in csv_file_paths:
        data = defaultdict(list)

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames

            for row in reader:
                json_objects = defaultdict(dict)
                for header in headers:
                    if '.' in header:
                        filename, json_key = parse_header(header)
                        if json_key:
                            nested_keys = json_key.split('.')
                            set_value(json_objects[filename], nested_keys, row[header])

                # Add the created JSON objects to the data
                for filename, json_obj in json_objects.items():
                    data[filename].append(json_obj)

        write_json_files(data, written_files, output_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file1> <csv_file2> ...")
        sys.exit(1)

    csv_file_paths = sys.argv[1:]
    output_dir = os.path.join("..", "test_database", "jct")  # Output directory one level up
    csv_to_json(csv_file_paths, output_dir)

