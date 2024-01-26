#!/usr/bin/env python3

import sys
import csv
import argparse
import os
import subprocess

def parse_passformat(input_string):
    """
    Parses the input string in passformat and returns a dictionary with keys URL, Username, Password, and TOTP.
    Stop parsing after the otpauth line; if no otpauth line exists, stop parsing after the URL line.
    """
    lines = input_string.strip().split('\n')
    pass_data = {'Password': lines[0].strip(), 'TOTP': ''}

    for line in lines[1:]:
        key, value = line.split(':', 1) if ':' in line else (line, '')
        key = key.strip()

        if key.startswith('otpauth://'):
            pass_data['TOTP'] = key
            break
        elif key in ['URL', 'Username']:
            pass_data[key] = value.strip()
        if key == 'URL':
            break

    return pass_data

def write_csv(folder, favorite, type, name, notes, fields, reprompt, pass_data, filename='output.csv'):
    """
    Writes the pass data to a CSV file with the specified name, appending if the file exists and has the correct header.
    """
    header = ['folder', 'favorite', 'type', 'name', 'notes', 'fields', 'reprompt', 'login_uri', 'login_username', 'login_password', 'login_totp']
    row = [folder, favorite, type, name, notes, fields, reprompt, pass_data.get('URL', ''), pass_data.get('Username', ''), pass_data['Password'], pass_data.get('TOTP', '')]

    if os.path.exists(filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            existing_header = next(reader, None)
            if existing_header != header:
                # Header does not match, overwrite the file
                mode = 'w'
            else:
                # Header matches, append to the file
                mode = 'a'
    else:
        mode = 'w'

    with open(filename, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow(header)
        writer.writerow(row)

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description='Convert passformat data to CSV format. Retrieves data using the pass utility and converts it to a specified CSV format.',
        epilog="""
        Usage examples:
        ./pass2bitwarden --pass_entry "my_pass_entry" --name "Example Site" --folder "Personal" --type "Login"
        ./pass2bitwarden --pass_entry "another_pass_entry" --name "Another Site" --favorite "Yes" --notes "My notes"
        
        Note: The pass utility must be installed and configured on your system.
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--pass_entry', help='The pass entry to retrieve data from', required=True)
    parser.add_argument('--folder', help='Folder field value for the CSV', required=False, default='')
    parser.add_argument('--favorite', help='Favorite field value for the CSV', required=False, default='')
    parser.add_argument('--type', help='Type field value for the CSV', required=False, default='')
    parser.add_argument('--name', help='Name field value for the CSV', required=True)
    parser.add_argument('--notes', help='Notes field value for the CSV', required=False, default='')
    parser.add_argument('--fields', help='Fields field value for the CSV', required=False, default='')
    parser.add_argument('--reprompt', help='Reprompt field value for the CSV', required=False, default='')

    args = parser.parse_args()

    # Retrieve pass data using the pass utility
    try:
        pass_data = subprocess.check_output(['pass', args.pass_entry], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving pass data: {e}")
        sys.exit(1)

    # Parse the passformat data
    pass_data = parse_passformat(pass_data)

    # Write to CSV
    write_csv(args.folder, args.favorite, args.type, args.name, args.notes, args.fields, args.reprompt, pass_data)

if __name__ == '__main__':
    main()
