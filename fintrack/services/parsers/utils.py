def format_key(key):
    # Replace spaces with underscores and convert to lowercase
    formatted_key = key.strip().replace(" ", "_").lower()
    
    # Ensure the key doesn't start with a number (Python variables can't start with numbers)
    if formatted_key and formatted_key[0].isdigit():
        formatted_key = "_" + formatted_key
    
    return formatted_key


def array_to_dict(arr):
    
    if len(arr) % 2 != 0:
        return "Array length is not even"
    
    formatted_keys = [format_key(key) if isinstance(key, str) else key for key in arr[::2]]
    return dict(zip(formatted_keys, arr[1::2]))
