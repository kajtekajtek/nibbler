from header import *

if __name__ == '__main__':
    is_running = True

    handle_args()

    # open file and read its contents
    file_name = sys.argv[1]
    contents = open_file(file_name)

    print_contents(contents)

