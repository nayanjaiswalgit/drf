satement_prompt = """

I have a bank statement with several transactions. I need the data extracted into JSON format. Each transaction should include the following details:

reference_number: The unique reference ID for the transaction.
amount: The transaction amount (positive for credits, negative for debits).
is_credit: A boolean value (true for credit transactions, false for debit transactions).
date: The transaction date in the format YYYY-MM-DD.
description: Any additional information or description available in the bank statement.
Additionally, I need the following:

account_no: The account number (this could be a card number, wallet ID, or bank account number).
The final JSON structure should look like this:

json
Copy code
{
  "account_no": "1234567890", 
  "transactions": [
    {
      "reference_number": "TXN123456",
      "amount": 1000.50,
      "is_credit": true,
      "date": "2024-12-10",
      "description": "Deposit from XYZ Corp"
    },
    {
      "reference_number": "TXN123457",
      "amount": 200.00,
      "is_credit": false,
      "date": "2024-12-11",
      "description": "Purchase at ABC Store"
    },
    {
      "reference_number": "TXN123458",
      "amount": 50.75,
      "is_credit": false,
      "date": "2024-12-12",
      "description": "ATM withdrawal"
    }
  ]
}
Please ensure the data is well-structured and organized in this format.
"""