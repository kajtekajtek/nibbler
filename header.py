import sys
import binascii

option_flags = []

def open_file(file_name):
    try:
        with open(file_name, 'rb') as f:
            # type(contents) = <class 'bytes'>
            contents = f.read()
            # bytes to hexadecimal notation conversion
            hex_contents = binascii.hexlify(contents).decode('utf-8')
            return hex_contents
    except:
        print(f"Error - couldn't open file {file_name}")

def handle_args():
    if len(sys.argv) < 2:
        print("Invalid amount of arguments - use nibbler.py -h for help")
        exit()

def print_contents(contents, page_num=0):
    # line indexing
    for i in range(page_num*256, page_num*256 + 256, 16):
        print('%07x'%i + " " + line_contents)
