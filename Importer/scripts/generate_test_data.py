"""
This script is useful to generate json data files by reading the data file as csv.
The script generates output at test_database/jct directory at one level above the scripts directory.

Usage:
    python generate_test_data.py [<csv_file1> <csv_file2> ... ]

"""

import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
import random

def calculate_issn_check_digit(issn):
    """Calculate the ISSN check digit for the first seven ISSN digits."""
    sum_of_digits = sum((8 - i) * int(digit) for i, digit in enumerate(issn))
    remainder = sum_of_digits % 11
    check_digit = 0 if remainder == 0 else 11 - remainder
    # Actual checksum digit would be 'X' if check_digit == 10 else str(check_digit)
    # return a fake checksum so that generated issn will not match with real issn
    return '1' if check_digit == 10 or check_digit == 0 else str(check_digit - 1)


def generate_issn():
    """Generate a valid ISSN."""
    first_seven_digits = ''.join(str(random.randint(0, 9)) for _ in range(7))
    check_digit = calculate_issn_check_digit(first_seven_digits)
    return f"{first_seven_digits[:4]}-{first_seven_digits[4:]}{check_digit}"

def generate_created_at():
    """Generate a dynamic creation datetime string in ISO 8601 format."""
    now = datetime.utcnow() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23),
                                        minutes=random.randint(0, 59))
    return now.strftime('%Y-%m-%dT%H:%M:%SZ')

def parse_header(header):
    """ Parse the header to get the filename and the JSON key. """
    parts = header.split('.')
    return parts[0], '.'.join(parts[1:]) if len(parts) > 1 else None

counter = 0

def generate_random_title_and_publisher():
    """Generate a random title and publisher from predefined lists."""
    global counter
    counter = counter + 1
    title = "Test title " + str(counter)
    publisher = "Test publisher " +str(counter)
    return title, publisher

def generate_jac_entry(issn):
    """Generate an entry for jac.json with test data."""
    title, publisher = generate_random_title_and_publisher()
    return {
        "issns": [issn],
        "title": title,
        "publisher": publisher,
        "index": {
            "issns": [issn, issn.replace("-", "")],
            "title": [title.lower()],
            "alts": [title.lower()]
        }
    }

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

    # Open jac.json file for writing if journal data is present and prepare it for writing
    journal_filename = "journal"
    jac_filename = "jac"
    # Check if there's data for journal (case-insensitive) to process
    journal_data_present = any(filename.lower() == journal_filename for filename in data.keys())
    if journal_data_present:
        jac_file_path = os.path.join(output_dir, f"{jac_filename}.json")
        mode = 'a' if jac_filename in written_files else 'w'
        jac_file = open(jac_file_path, mode, encoding='utf-8')

    for filename, contents in data.items():
        file_path = os.path.join(output_dir, f"{filename}.json")
        mode = 'a' if filename in written_files else 'w'
        with open(file_path, mode, encoding='utf-8') as json_file:
            for content in contents:
                if filename.lower() == journal_filename:
                    issn = generate_issn()
                    content.update({"issn": [issn], "createdAt": generate_created_at()})
                    # Directly write the corresponding jac entry
                    jac_entry = generate_jac_entry(issn)
                    json.dump(jac_entry, jac_file)
                    jac_file.write('\n')
                json.dump(content, json_file)
                json_file.write('\n')
        written_files.add(filename)

    if journal_filename in data:
        jac_file.close()
        written_files.add(jac_filename)

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
    output_dir = os.path.join("..", "test_database")  # Output directory one level up
    csv_to_json(csv_file_paths, output_dir)
