import sys
from os import system, name
import binascii

vars = {
        # by default every page contains 16 lines made of 32 characters
        "line_length":32, # (16 bytes)
        "page_size":16,
        "column_width":4,
        "current_page":0
        }

# raw_contents = variable of the bytes type containing original file contents
def processContents(raw_contents):
    line_length = vars["line_length"]
    page_size = vars["page_size"]

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

def openReadFile(file_name):
    try:
        with open(file_name, 'rb') as f:
            contents = processContents(f.read())
            return contents
    except Exception as error:
        print(f"Error - couldn't open file {file_name}")
        print(error)

def openWriteFile(file_name, contents):
    contents_string = ""
    for page in contents:
        for line in page:
            contents_string += line

    # return binary data
    contents_raw = binascii.unhexlify(contents_string)

    try:
        with open(file_name, 'wb') as f:
            f.write(contents_raw)
            print("Changes saved")
    except Exception as error:
        print(f"Error - couldn't open file {file_name}")
        print(error)

def handleArgs():
    if len(sys.argv) < 2:
        print("Invalid amount of arguments - use nibbler.py -h for help")
        exit()

def printPage(contents, page_index=0):
    line_length = vars["line_length"]
    page_size = vars["page_size"]

    # first byte of the line index (hexdump-like)
    byte_index = page_index * page_size * int(line_length/2)

    for line in contents[page_index]:
        # C string style of formating for padding the first byte of the 
        # line index
        line_to_print = '%07x'%byte_index + " "
        # printing contents as column_width wide columns
        line_to_print += " ".join(line[i:i+vars["column_width"]] for i in range(0, len(line), vars["column_width"]))

        print(line_to_print)

        byte_index += int(line_length / 2)

# clear screen
def clear():
    # windows
    if name == "nt":
        _ = system("cls")
    # unix
    else:
        _ = system('clear')

# calculate page index from byte address
def pageIndexFromAddr(addr):
    addr = int(addr, 16)
    page_size = vars["page_size"]
    line_length = int(vars["line_length"] / 2)
    
    page_addr = addr - (addr % (page_size*line_length))
    page_index = page_addr / (page_size * line_length)

    return int(page_index)

def replaceByte(page_index):
    try:
        val = int(input())
        hex_val = hex(val)
        hex_string = str(hex_val)
    except:
        print(1)

def userInput(contents):
    try:
        ch = input()
    except:
        return

    match ch.split():
        # show next page
        case ['n']:
            if vars["current_page"] < len(contents) - 1:
                vars["current_page"] += 1
                clear()
                printPage(contents, 1)
        # show previous page
        case ['p']:
            if vars["current_page"] > 0:
                vars["current_page"] -= 1
                clear()
                printPage(contents, vars["current_page"])
        # go to address
        case ['goto', *_]:
            args = ch.split()
            try:
                page_index = pageIndexFromAddr(args[1])
                if page_index in range(len(contents)):
                    clear()
                    vars["current_page"] = page_index
                    printPage(contents, vars["current_page"])
                else:
                    print("Out of range address")
            except Exception as error:
                print("usage: goto [address]")
        case ['r', *_]:
            args = ch.split()
            try:
                page_index = pageIndexFromAddr(args[1])
                line_index = args[1] 
                if page_index in range(len(contents)):
                    replaceByte(page_index)
                else:
                    print("Out of range address")
            except Exception as error:
                print("usage: r [address]")

        case ['w']:
            openWriteFile(vars["file_name"], contents)
        case ['wq']:
            openWriteFile(vars["file_name"], contents)
            clear()
            exit()
        # help
        case ['h']:
            print("n - next page")
            print("p - previous page")
            print("goto [address] - go to specified position")
            print("r [addr] - edit bytes on specified addr")
            print("w - write")
            print("wq - write and quit")
            print("q - quit")
        # quit
        case ['q']:
            clear()
            exit()
        # default case
        case _:
            print("Unknown command")

