import pdfplumber
import json

import re

def format_key(key):
    """Formats the key to follow Python variable naming conventions:
    - Lowercase
    - Replaces spaces with underscores
    - Ensures the key doesn't start with a number
    
    Args:
        key (str): The original key to format.
        
    Returns:
        str: The formatted key.
    """
    # Replace spaces with underscores and convert to lowercase
    formatted_key = key.strip().replace(" ", "_").lower()
    
    # Ensure the key doesn't start with a number (Python variables can't start with numbers)
    if formatted_key and formatted_key[0].isdigit():
        formatted_key = "_" + formatted_key
    
    return formatted_key



def process_transactions(row_data):
    # Function to remove commas and convert to float

    def convert_to_float(value):
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return 0.0  # Return 0.0 if the conversion fails

    # Extract details from the row
    
    reference_number = row_data.get("cheque/reference\nno") or None
    particulars = row_data.get("particulars", "")
    debit = row_data.get("debit", "0.00")
    credit = row_data.get("credit", "0.00")
    balance = row_data.get("balance", "0.00")
    sr_no = row_data.get("sr_no", "0")
    date = row_data.get("date", "")
    channel = row_data.get("channel", "")

    # If reference_number is None, try to extract it from the 'particulars'
    if reference_number is None:
        match = re.match(r"(\d+)", particulars)
        if match:
            reference_number = match.group(1)
            description = particulars[match.end():].strip()  # Rest of the particulars as description
        else:
            reference_number = particulars.replace("\n", " ").strip().split()[-1]
            description = ""  # If no match, use the entire 'particulars' as description
    else:
        description = particulars  # If reference_number exists, use 'particulars' as description

        # If reference_number exists, remove it from the description
        description = description.replace(reference_number, "").strip()

    # Remove any newline characters from the description
    description = description.replace("\n", " ").strip() 
    
    description =' '.join(sorted(set(description.strip("'").split()), key=description.index))
    # Convert debit, credit, and balance values to float (remove commas first)
    debit = convert_to_float(debit)
    credit = convert_to_float(credit)
    balance = convert_to_float(balance)

    # Calculate the amount (debit if no credit)
    amount = debit if debit > 0 else credit

    # Determine if it is a credit transaction (credit > 0)
    is_credit = True if credit > 0 else False

    # Return the desired format
    return {
        "sr_no" : sr_no,
        "reference_number": reference_number,
        "amount": amount,
        "is_credit": is_credit,
        "date": date,
        "description": description
    }


def array_to_dict(arr):
    """Converts an array to a dictionary by pairing elements (even index as keys, odd as values).
    
    Args:
        arr (list): Input array to convert to dictionary.
        
    Returns:
        dict or str: Dictionary if array length is even, error message  otherwise.
    """
    if len(arr) % 2 != 0:
        return "Array length is not even"
    
    formatted_keys = [format_key(key) if isinstance(key, str) else key for key in arr[::2]]
    return dict(zip(formatted_keys, arr[1::2]))


def parse_bofm_statement(pdf_file_path):
    """Extracts and converts PDF tables to JSON format.
    
    Args:
        pdf_file_path (str): Path to the PDF file.
        
    Returns:
        list: A list containing both 'transactions' and 'other_tables' as separate dictionaries.
    """
    transactions_columns = ['Sr No', 'Date', 'Particulars', 'Cheque/Reference\nNo', 'Debit', 'Credit', 'Balance', 'Channel']
    
    data = {}  # This will hold both transactions and other tables as separate entries
    
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                # Extract tables from the page
                tables = page.extract_tables()
                
                for table in tables:
                    if not table:
                        continue  # Skip empty tables
                    
                    columns = table[0]  # First row as column headers
                    
                    # Check if the table corresponds to transactions
                    if columns == transactions_columns:
                        transactions = []
                        for row in table[1:]:
                            row_dict = dict(zip(columns, row))
                            row_dict = {format_key(key): value for key, value in row_dict.items() if key and value}
                            row_dict = process_transactions(row_dict)
                            transactions.append(row_dict)
                        
                        # Append transactions as a separate entry
                        if transactions:
                            data.update({'transactions': transactions})
                    else:
                        # Handle other tables by creating a dictionary for each row
                        other_table = {}
                        for row in table[1:]:
                            row_dict = array_to_dict(row)
                            if isinstance(row_dict, dict) and row_dict:  # Avoid empty dictionaries
                                # Sanitize the table key and add to the result
                                table_key = format_key(columns[0]) if columns[0] else None
                                if table_key:
                                    other_table.update(row_dict)
                        if other_table:  # Avoid appending empty tables
                            data.update({table_key: other_table})
            
    except FileNotFoundError:
        print(f"Error: The file '{pdf_file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return json.dumps(data, indent=4)



# Example usage:
json_string = parse_bofm_statement('test.pdf')

json_data = json.loads(json_string)

formated_data = {}

if "transactions" in json_data:
    formated_data.update({"transactions": json_data["transactions"]})
    
if "account_details" in json_data:
    formated_data.update({"account_no": json_data["account_details"]["account_no"]})
    
if "total_transaction_count" in json_data:
    formated_data.update({"summary": json_data["total_transaction_count"]})

print(formated_data)
