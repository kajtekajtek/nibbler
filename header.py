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

# open and read from a file
def openReadFile(file_name):
    try:
        with open(file_name, 'rb') as f:
            contents = processContents(f.read())
            return contents
    except Exception as error:
        print(f"Error - couldn't open file {file_name}")
        print(error)

# open and write to a file
def openWriteFile(file_name, contents):
    contents_string = ""
    for page in contents:
        for line in page:
            contents_string += line

    # return to binary data
    contents_raw = binascii.unhexlify(contents_string)

    try:
        with open(file_name, 'wb') as f:
            f.write(contents_raw)
            print("Changes saved")
    except Exception as error:
        print(f"Error - couldn't open file {file_name}")
        print(error)

# handling command line arguments
def handleArgs():
    if len(sys.argv) < 2:
        print("Invalid amount of arguments - use nibbler.py -h for help")
        exit()

# print page of the contents
def printPage(contents, page_index=0):
    line_length = vars["line_length"]
    page_size = vars["page_size"]

    # address of the first byte on the line (hexdump-like)
    byte_index = page_index * page_size * int(line_length/2)

    for line in contents[page_index]:
        # C string style of formating for padding the address with 0s 
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

def replaceSingleByte(contents, page_index, addr):
    page_size = vars["page_size"]
    line_length = int(vars["line_length"]/2)

    try:
        addr = int(addr, 16)

        line_index = int((addr % (page_size * line_length)) / line_length)

        byte_index = addr % line_length
        byte_index = (byte_index * 2)

        if byte_index in range(len(contents[page_index][line_index])):
            val = input("New value (hexadecimal): ")

            if int(val, 16) in range(256):
                # replacing values
                line = contents[page_index][line_index]
                line = line[:byte_index] + val.lower() + line[byte_index + 2:]
                contents[page_index][line_index] = line
            else:
                print("Out of range value")
                return
        else:
            print("Out of range value")
            return
    except Exception as error:
        print("Couldn't perform replace operation")
    
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
        # replace single byte
        case ['r', *_]:
            args = ch.split()
            try:
                addr = args[1] 
                page_index = pageIndexFromAddr(addr)
                if page_index in range(len(contents)):
                    vars["current_value"] = page_index

                    clear()
                    printPage(contents, vars["current_value"])

                    replaceSingleByte(contents, page_index, addr)

                    clear()
                    printPage(contents, vars["current_value"])
                else:
                    print("Out of range address")
            except Exception as error:
                print("usage: r [address]")
                print(error)
        # change the number of bytes displayed in one column
        case ['column', 'width', *_]:
            args = ch.split()
            if len(args) == 3:
                try:
                    val = int(args[2])
                    if int(val) > 0:
                        vars["column_width"] = val*2
                        clear()
                        printPage(contents, vars["current_page"])
                    else:
                        raise Exception
                except Exception as error:
                    print("invalid column width value")
            else:
                print("usage: column width [value]")
        case ['w', *_]:
            args = ch.split()
            if len(args) == 1:
                openWriteFile(vars["file_name"], contents)
            elif len(args) == 2:
                openWriteFile(args[1], contents)
            else:
                print("usage: w [filename(optional)]")
        case ['wq']:
            openWriteFile(vars["file_name"], contents)
            clear()
            exit()
        # help
        case ['h']:
            print("n - next page")
            print("p - previous page")
            print("goto [address] - go to specified position")
            print("r [addr] - replace byte on specified address")
            print("column width [value] - change the number of bytes displayed in one column")
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

