from header import *

if __name__ == '__main__':
    handleArgs()

    # open file and read its contents
    file_name = sys.argv[1]
    contents = openFile(file_name)

    clear()
    printPage(contents)

    while True:
        userInput(contents)

