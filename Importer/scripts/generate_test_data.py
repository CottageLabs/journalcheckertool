"""
This script is useful to generate json data files by reading the data file as csv.
The script generates output at test_database/jct directory at one level above the scripts directory.

Usage:
    python generate_test_data.py [<csv_file1> <csv_file2> ... ]

"""
import argparse
import ast
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
import random
from jctdata import settings
import constants

journal_filename = "journal"
funder_filename = "funder_config"
funder_lang_filename = "funder_language"
jac_filename = "jac"
iac_filename = "iac"
institution_filename = "institution"
testrecords = defaultdict(list)

counter = 0
institution_counter = 0
funder_counter = 0
countries = ["United States", "Canada", "United Kingdom", "France", "Germany", "Japan", "Australia"]


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


def generate_ror_id():
    ror_id = "".join(random.choice('0123456789abcdef') for _ in range(9))
    return ror_id


def generate_created_at():
    """Generate a dynamic creation datetime string in ISO 8601 format."""
    now = datetime.utcnow() - timedelta(days=random.randint(0, 365), hours=random.randint(0, 23),
                                        minutes=random.randint(0, 59))
    return now.strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_header(header):
    """ Parse the header to get the filename and the JSON key. """
    parts = header.split('.')
    return parts[0].lower(), '.'.join(parts[1:]) if len(parts) > 1 else None


def generate_random_title_and_publisher():
    """Generate a random title and publisher from predefined lists."""
    global counter
    counter = counter + 1
    title = "Test title " + str(counter)
    publisher = "Test publisher " + str(counter)
    return title, publisher


def generate_random_title_and_country():
    """Generate a random title and country from predefined lists for institution."""
    global institution_counter
    institution_counter = institution_counter + 1
    title = "Test University " + str(institution_counter)
    country = random.choice(countries)
    return title, country


def generate_funder_id_name():
    """Generate a random id and name for funder."""
    global funder_counter
    funder_counter = funder_counter + 1
    funder_id = "test_funder_" + str(funder_counter)
    name = "Test Funder " +str(funder_counter)
    return funder_id, name


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


def generate_iac_entry(ror):
    """Generate an entry for jac.json with test data."""
    title, country = generate_random_title_and_country()
    return {
        "ror": ror,
        "title": title,
        "country": country,
        "index": {
            "title": [title.lower()],
            "ror": ror
        }
    }


def set_value(dct, keys, value):
    """ Set a value in a nested dictionary based on a list of keys. """
    for key in keys[:-1]:
        if key not in dct or not isinstance(dct[key], dict):
            dct[key] = {}
        dct = dct[key]
    dct[keys[-1]] = value if value != '' else None


def get_funder_data(route, data):
    FUNDER_ROW = {"routes": {"self_archiving": {"calculate": True, "rights_retention": "2022-11-01T00:00:00Z",
                "license": ["cc-by", "cc-by-sa", "cc0"], "embargo": 0}, "fully_oa": {"calculate": True,
                "license": ["cc-by", "cc-by-sa", "cc0"]}, "hybrid": {"calculate": False,
                "license": ["cc-by", "cc-by-sa", "cc0"]}, "ta": {"calculate": True,
                "license": ["cc-by", "cc-by-sa", "cc0"]}, "tj": {"calculate": True}},
                "card_order": ["fully_oa", "fully_oa_by_exception", "ta", "ta_aq", "tj", "self_archiving", "sa_rr",
                               "journal_non_compliant", "funder_non_compliant", "institution_non_compliant",
                               "rights_retention_non_compliant"],
                "cards": [{"id": "fully_oa", "compliant": True, "match_routes": {"must": ["fully_oa"]},
                           "match_qualifications": {"not": ["fully_oa.oa_exception_caveat"]}, "preferred": False},
                          {"id": "fully_oa_by_exception", "compliant": True, "match_routes": {"must": ["fully_oa"]},
                           "match_qualifications": {"must": ["fully_oa.oa_exception_caveat"]}, "preferred": False},
                          {"id": "sa_rr", "compliant": True, "match_routes": {"must": ["self_archiving"],
                            "not": ["fully_oa"]}, "match_qualifications":
                              {"must": ["self_archiving.rights_retention_author_advice"]}, "preferred": False,
                           "modal": "sa_rr"}, {"id": "self_archiving", "compliant": True, "match_routes":
                        {"must": ["self_archiving"], "not": ["fully_oa"]},
                        "match_qualifications": {"not": ["self_archiving.rights_retention_author_advice"]},
                        "preferred": False, "modal": "sa"}, {"id": "ta", "compliant": True, "match_routes":
                        {"must": ["ta"]}, "match_qualifications": {"not": ["ta.corresponding_authors"]},
                        "preferred": False}, {"id": "ta_aq", "compliant": True, "match_routes": {"must": ["ta"]},
                        "match_qualifications": {"must": ["ta.corresponding_authors"]}, "preferred": False},
                        {"id": "tj", "compliant": True, "match_routes": {"must": ["tj"]}, "preferred": False,
                        "modal": "tj"}, {"id": "journal_non_compliant", "compliant": False, "match_routes":
                        {"not": ["self_archiving", "fully_oa", "ta", "tj"]}, "preferred": False},
                        {"id": "funder_non_compliant", "compliant": False, "match_routes":
                        {"not": ["self_archiving", "fully_oa", "ta", "tj"]}, "preferred": False},
                        {"id": "institution_non_compliant", "compliant": False, "match_routes": {"not":
                        ["self_archiving", "fully_oa", "ta", "tj"]}, "preferred": False},
                          {"id": "rights_retention_non_compliant", "compliant": False, "match_routes":
                        {"not": ["self_archiving", "fully_oa", "ta", "tj"]}, "preferred": False}],
                  "id": "testid", "name": "Test Funder", "abbr": "SNSF", "plan_s": "2022-11-01T00:00:00Z",
                  "apc": {"tj": False}}

    for key, value in data.items():
        if value:
            FUNDER_ROW["routes"][route][key] = value
            # funder_id, name = generate_funder_id_name()
        elif key.lower() == 'rights_retention':
            FUNDER_ROW['routes']['self_archiving']['rights_retention'] = '2050-01-17T00:00:00Z'

    FUNDER_ROW["id"] = data["id"]
    FUNDER_ROW["name"] = data["name"]

    return FUNDER_ROW


def get_lang_data(lang, data):
    lang = lang.lower()
    lang_data = None
    if lang == "en":
        lang_data = constants.FUNDER_LANG_EN
    elif lang == "fr":
        lang_data = constants.FUNDER_LANG_FR

    if lang_data:
        lang_data["id"] = data["id"] + "__" + lang

    return lang_data


def write_json_files(route, data, written_files, output_dir):
    """ Write the organized data to JSON files, each JSON object in a single line. """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if there's data for journal (case-insensitive) to process
    journal_data_present = any(filename.lower() == journal_filename for filename in data.keys())
    if journal_data_present:
        # Open jac.json file for writing if journal data is present and prepare it for writing
        jac_file_path = os.path.join(output_dir, f"{jac_filename}.json")
        mode = 'a' if jac_filename in written_files else 'w'
        jac_file = open(jac_file_path, mode, encoding='utf-8')
        if mode == 'w':
            written_files.add(jac_filename)

    # Check if there's data for institution (case-insensitive) to process
    institution_data_present = any(filename.lower() == institution_filename for filename in data.keys())
    if institution_data_present:
        # Open jac.json file for writing if journal data is present and prepare it for writing
        iac_file_path = os.path.join(output_dir, f"{iac_filename}.json")
        mode = 'a' if iac_filename in written_files else 'w'
        iac_file = open(iac_file_path, mode, encoding='utf-8')
        if mode == 'w':
            written_files.add(iac_filename)

    # Check if there's data for institution (case-insensitive) to process
    funder_config_present = any(filename.lower() == funder_filename for filename in data.keys())
    if funder_config_present:
        # Open funder_language.json file for writing if journal data is present and prepare it for writing
        funder_lang_file_path = os.path.join(output_dir, f"{funder_lang_filename}.json")
        mode = 'a' if funder_lang_file_path in written_files else 'w'
        funder_lang_file = open(funder_lang_file_path, mode, encoding='utf-8')
        if mode == 'w':
            written_files.add(funder_lang_filename)

    for filename, contents in data.items():
        file_path = os.path.join(output_dir, f"{filename}.json")
        mode = 'a' if filename in written_files else 'w'
        with open(file_path, mode, encoding='utf-8') as json_file:
            for content in contents:
                if filename.lower() == journal_filename:
                    content.update({"createdAt": generate_created_at()})
                    # write the corresponding jac entry
                    jac_entry = generate_jac_entry(content["issn"])
                    json.dump(jac_entry, jac_file)
                    jac_file.write('\n')

                    json.dump(content, json_file)
                    json_file.write('\n')

                elif filename.lower() == funder_filename:
                    funder_data = get_funder_data(route, content)
                    # write data to funder config the funder data available
                    if funder_data:
                        json.dump(funder_data, json_file)
                        json_file.write('\n')

                    # Write funder language data
                    funder_lang_data_en = get_lang_data("en", content)
                    funder_lang_data_fr = get_lang_data("fr", content)
                    if funder_lang_data_en:
                        json.dump(funder_lang_data_en, funder_lang_file)
                        funder_lang_file.write('\n')
                    if funder_lang_data_fr:
                        json.dump(funder_lang_data_fr, funder_lang_file)
                        funder_lang_file.write('\n')

                elif filename.lower() == institution_filename:
                    # write the corresponding jac entry
                    iac_entry = generate_iac_entry(content["ror"])
                    json.dump(iac_entry, iac_file)
                    iac_file.write('\n')

                    json.dump(content, json_file)
                    json_file.write('\n')
                else:
                    json.dump(content, json_file)
                    json_file.write('\n')
        written_files.add(filename)

    if journal_filename in data:
        jac_file.close()
        written_files.add(jac_filename)


def parse_value(value: str):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    else:
        return ast.literal_eval(value)


def csv_to_json(route, csv_file_path, output_dir, written_files):

    data = defaultdict(list)

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        for row in reader:
            journal_id = ""
            funder_id = ""
            institution_id = ""

            json_objects = defaultdict(dict)
            for header in headers:
                if '.' in header:
                    filename, json_key = parse_header(header)
                    if json_key:
                        nested_keys = json_key.split('.')

                        try:
                            set_value(json_objects[filename], nested_keys, parse_value(row[header]))
                        except:
                            print("route : " + route + " header : " + header + " value : " + row[header])
                            set_value(json_objects[filename], nested_keys, row[header])

            if journal_filename in json_objects:
                journal_id = generate_issn()
                set_value(json_objects[journal_filename], ["issn"], journal_id)
            if institution_filename in json_objects:
                institution_id = generate_ror_id()
                set_value(json_objects[institution_filename], ["ror"], institution_id)
            if funder_filename in json_objects:
                funder_id, name = generate_funder_id_name()
                set_value(json_objects[funder_filename], ["id"], funder_id)
                set_value(json_objects[funder_filename], ["name"], name)

            # Add the created JSON objects to the data
            for filename, json_obj in json_objects.items():
                data[filename].append(json_obj)

            testrecords[row["Test"]] = dict(journal=journal_id, institution=institution_id, funder=funder_id)

    write_json_files(route, data, written_files, output_dir)


def write_test_records():
    file_path = os.path.join(output_dir, "test_records.json")
    with open(file_path, "w", encoding='utf-8') as records_file:
        json.dump(testrecords, records_file, indent=2)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file1> <csv_file2> ...")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Generate JSON files from specified CSV inputs.")
    parser.add_argument("--self_archiving", help="Path to the self_archiving CSV file", type=str)
    parser.add_argument("--fully_oa", help="Path to the fully_oa CSV file", type=str)
    parser.add_argument("--hybrid", help="Path to the hybrid CSV file", type=str)
    parser.add_argument("--ta", help="Path to the ta CSV file", type=str)
    parser.add_argument("--tj", help="Path to the tj CSV file", type=str)

    args = parser.parse_args()

    written_files = set()
    output_dir = settings.TEST_DATABASE  # Output directory
    funderdb_funders_dir = os.path.join("..", "..", "funderdb", "funders")

    # Handle each specified CSV file
    file_paths = [{"self_archiving": args.self_archiving}, {"fully_oa": args.fully_oa},
                  {"hybrid": args.hybrid}, {"ta": args.ta}, {"tj": args.tj}]  # Add other files as needed
    for file_path in file_paths:
        for key, value in file_path.items():
            if value:
                csv_to_json(key, value, output_dir, written_files)
    write_test_records()
