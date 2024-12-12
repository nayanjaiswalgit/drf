from .statement_parser import parse_bofm_statement

def get_statement_parser(bank_name):
    if bank_name == 'bank_of_maharastra':
        return parse_bofm_statement
    else:
        return None