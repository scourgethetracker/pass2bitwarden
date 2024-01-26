
# Pass to Bitwarden CSV Converter Script

## Overview
This Python script is designed to convert password data in a custom format (referred to as "passformat") into a CSV file. It's particularly useful for managing password entries that are retrieved using the `pass` command-line utility. The script allows for appending the data to an existing CSV file, ensuring the correct format with no duplication of the header row.

## Requirements
- Python 3
- The `pass` command-line utility installed and configured

## Usage
The script accepts command-line arguments to specify the pass entry and additional metadata for the CSV output. It retrieves the pass data, parses it, and writes it to a CSV file.

### Command Line Arguments
- `--pass_entry`: The pass entry to retrieve data from (required).
- `--folder`: Folder field value for the CSV (optional).
- `--favorite`: Favorite field value for the CSV (optional).
- `--type`: Type field value for the CSV (optional).
- `--name`: Name field value for the CSV (required).
- `--notes`: Notes field value for the CSV (optional).
- `--fields`: Fields field value for the CSV (optional).
- `--reprompt`: Reprompt field value for the CSV (optional).

### Usage Examples
```bash
./pass2bitwarden.py --pass_entry "my_pass_entry" --name "Example Site" --folder "Personal" --type "Login"
./pass2bitwarden.py --pass_entry "another_pass_entry" --name "Another Site" --favorite "Yes" --notes "My notes"
```

## Input Format ("passformat")
The input data is expected in the following format (referred to as "passformat"):
```
Password
Username: someusername
URL: https://someurl.com
otpauth://...
```

- The first line contains the password.
- Subsequent lines contain other fields like username, URL, and otpauth, each prefixed with their field name and a colon.

## Output Format (CSV)
The output is a CSV file with the following columns:
- `folder`
- `favorite`
- `type`
- `name`
- `notes`
- `fields`
- `reprompt`
- `login_uri`
- `login_username`
- `login_password`
- `login_totp`

### Example CSV Output
```
folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp
Personal,,Login,Example Site,,,,https://someurl.com,someusername,Password,otpauth://...
```

## Note
This script assumes the `pass` utility is properly configured and accessible on your system. The script will retrieve the specified pass entry and convert it into the desired CSV format.
