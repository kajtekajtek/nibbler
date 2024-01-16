from header import *

if __name__ == '__main__':
        handleArgs()

        # open file and read its contents
        vars["file_name"] = sys.argv[1]
        contents = openReadFile(vars["file_name"])

        clear()
        printPage(contents)

        while True:
            userInput(contents)

