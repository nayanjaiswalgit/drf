import json
from bs4 import BeautifulSoup
import re

def is_valid_format(transaction_string):
    """
    Check if the transaction string contains all required fields.
    """
    required_patterns = [
        r"A/c No xx \d+",  # Account number
        r"(debited|credited) by INR [\d,]+\.\d{2}",  # Transaction amount
        r"\d{2}-[A-Za-z]{3}-\d{4}",  # Date in format DD-MMM-YYYY
        r"UPI RRN [:]?\d+",  # UPI RRN
        r"A/c Bal is INR [\d,]+\.\d{2}",  # Account balance
        r"AVL Bal is INR [\d,]+\.\d{2}"  # Available balance
    ]
    
    # Check if all required patterns are present in the string
    return all(re.search(pattern, transaction_string) for pattern in required_patterns)

def parse_transaction(transaction_string):
    """
    Parse the transaction string into a structured JSON format.
    """
    if not is_valid_format(transaction_string):
        return {"error": "Invalid format"}
    
    # Parse the HTML content
    soup = BeautifulSoup(transaction_string, 'html.parser')

    # Extract the text from the HTML
    text = soup.get_text(separator=" ")

    # Extract information using regex patterns
    account_number = re.search(r"A/c No xx (\d+)", text)
    transaction_amount = re.search(r"(debited|credited) by INR ([\d,]+\.\d{2})", text)
    date = re.search(r"(\d{2}-[A-Za-z]{3}-\d{4})", text)
    upi_rrn = re.search(r"UPI RRN [:]?(\d+)", text)
    account_balance = re.search(r"A/c Bal is INR ([\d,]+\.\d{2})", text)
    available_balance = re.search(r"AVL Bal is INR ([\d,]+\.\d{2})", text)
    bank_name = "Bank Of Maharashtra"
    
    # Create a dictionary to store the data
    transaction_data = {
        "account_number": account_number.group(1) if account_number else None,
        "transaction_amount": float(transaction_amount.group(2).replace(",", "")) if transaction_amount else None,
        "transaction_type": "Debit" if "debited" in text else "Credit",
        "date": date.group(1) if date else None,
        "upi_rrn": upi_rrn.group(1) if upi_rrn else None,
        "account_balance": float(account_balance.group(1).replace(",", "")) if account_balance else None,
        "available_balance": float(available_balance.group(1).replace(",", "")) if available_balance else None,
        "bank_name": bank_name
    }
    
    return transaction_data

# Example strings
debit_string = "<htm><body>Dear Customer,<br><br>Your A/c No xx 4388 debited by INR 6,994.00 on 02-DEC-2024 with UPI RRN :433782083496. A/c Bal is INR 2,42,853.15 CR and AVL Bal is INR 2,42,853.15 CR-MAHABANK<br><br>Yours Faithfully,</br><br>Bank Of Maharashtra <br><br><br><br><b>Please use our toll free numbers 1800 233 4526 and 1800 102 2636 for any banking related queries.</b><br><b>Connect with us on Facebook, Twitter, LinkedIn @mahabank</b><br><br></body><br></html>"
credit_string = "<htm><body>Dear Customer,<br><br>Your A/c No xx 4388 credited by INR 1,694.00 on 01-DEC-2024 with UPI RRN 433653619501. A/c Bal is INR 2,62,049.15 CR and AVL Bal is INR 2,62,049.15 CR-MAHABANK<br><br>Yours Faithfully,</br><br>Bank Of Maharashtra <br><br><br><br><b>Please use our toll free numbers 1800 233 4526 and 1800 102 2636 for any banking related queries.</b><br><b>Connect with us on Facebook, Twitter, LinkedIn @mahabank</b><br><br></body><br></html>"

# Parse the debit and credit strings
debit_transaction = parse_transaction(debit_string)
credit_transaction = parse_transaction(credit_string)

# Convert the parsed data to JSON
debit_json = json.dumps(debit_transaction, indent=4)
credit_json = json.dumps(credit_transaction, indent=4)

print("Debit Transaction JSON:\n", debit_json)
print("\nCredit Transaction JSON:\n", credit_json)
