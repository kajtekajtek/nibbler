from header import *

if __name__ == '__main__':
    is_running = True

    handleArgs()

    # open file and read its contents
    file_name = sys.argv[1]
    contents = openFile(file_name)

    printPage(contents, 0)

