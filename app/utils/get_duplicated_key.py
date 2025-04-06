import re
def get_duplicated_key(error_message: str) -> str:
    # Parsing the error message to extract the duplicated key

    # Use regular expression to extract the key name from the error message
    match = re.search(r'Key \((\w+)\)=', error_message)
    if match:
        duplicated_key_name = match.group(1)
        return duplicated_key_name
    else:
        return ""
