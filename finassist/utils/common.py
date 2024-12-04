import magic

def get_file_type(file):
    """
    Determine the file type (either PDF or Image) based on its MIME type using python-magic.
    Returns 'pdf' or 'image' if detected, otherwise None.
    """
    mime_type = magic.Magic(mime=True).from_buffer(file.read(2048))  # Read a portion to detect MIME type
    file.seek(0)  # Reset file pointer after reading

    # Return the file type based on MIME type, or None if unsupported
    if 'pdf' in mime_type:
        return 'pdf'
    elif 'image' in mime_type:
        return 'image'
    return None  # Return None if the MIME type is unsupported
