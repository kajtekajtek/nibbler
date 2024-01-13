import sys
import binascii

# by default every page contains 16 lines made of 32 characters (16 bytes)
options = {
        "line_length":32,
        "page_size":16
        }

# raw_contents = variable of the bytes type containing original file contents
def processContents(raw_contents):
    line_length = options["line_length"]
    page_size = options["page_size"]

    # bytes type -> bytes type, hexadecimal notation (hexlify()) 
    # -> utf-8 string (decode())
    contents_string = binascii.hexlify(raw_contents).decode('utf-8')

    contents = []

    # for every page made of page_size lines of line_length length 
    for i in range(0, len(contents_string), page_size * line_length):
        page = []
        # for every line
        for j in range(0, page_size * line_length, line_length):
            # from page index + line index position append next line_length
            # characters to the current page
            page.append(contents_string[i + j:i + j + line_length]) 

        contents.append(page)
    
    return contents

def openFile(file_name):
    try:
        with open(file_name, 'rb') as f:
            contents = processContents(f.read())
            return contents
    except Exception as error:
        print(f"Error - couldn't open file {file_name}")
        print(error)

def handleArgs():
    if len(sys.argv) < 2:
        print("Invalid amount of arguments - use nibbler.py -h for help")
        exit()

def printPage(contents, page_index=0):
    line_length = options["line_length"]
    page_size = options["page_size"]

    # first byte of the line index (hexdump-like)
    byte_index = page_index * page_size * line_length

    for line in contents[page_index]:
        # C string style of formating for padding the first byte of the 
        # line index
        print('%07x'%byte_index + " " + line)
        byte_index += int(line_length / 2)

