import re
import pandas as pd
from PyPDF2 import PdfReader

def fetch_parsing_rule(bank_name, file_type, rules_model):
    try:
        return rules_model.objects.get(bank_name=bank_name, file_type=file_type)
    except rules_model.DoesNotExist:
        return None

import pdfplumber
import pandas as pd

def parse_pdf_with_rule(file_path, test):
    # Open the PDF with pdfplumber
    with pdfplumber.open(file_path) as pdf:
        # Assuming the table is on the first page (you can loop through pages if needed)
        page = pdf.pages[0]
        
        # Extract the table from the page
        table = page.extract_table()

        # Check if a table was found
        if table:
            # Convert the table into a pandas DataFrame for easier manipulation
            df = pd.DataFrame(table[1:], columns=table[0])  # The first row is the header

            # Clean the DataFrame if needed, for example:
            # Convert strings to numbers, handle missing values, etc.
            df['Debit'] = pd.to_numeric(df['Debit'], errors='coerce')
            df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce')
            df['Balance'] = pd.to_numeric(df['Balance'], errors='coerce')
            return df
        else:
            print("No table found on the page.")
            return None

def parse_csv_with_rule(file_path, column_mapping):
    df = pd.read_csv(file_path)
    if column_mapping:
        df.rename(columns=column_mapping, inplace=True)
    return df.to_dict('records')

def parse_text_with_rule(file_path, regex_pattern):
    with open(file_path, 'r') as file:
        text = file.read()
    matches = re.findall(regex_pattern, text)
    return [
        {'date': match[0], 'amount': float(match[1].replace(',', '')), 'description': match[2]}
        for match in matches
    ]

def parse_file(file_path, rule):
    if rule.file_type == 'pdf':
        return parse_pdf_with_rule(file_path, rule.regex_pattern)
    elif rule.file_type == 'csv':
        return parse_csv_with_rule(file_path, rule.column_mapping)
    elif rule.file_type == 'txt':
        return parse_text_with_rule(file_path, rule.regex_pattern)
    else:
        raise ValueError("Unsupported file type.")
