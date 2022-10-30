import sys # for command-line arguments
import gzip # for unzipping gzipped files
import os # for file system

def xopp2xml(input_path: str, output_path: str):
    with gzip.open(input_path, "rt", encoding="utf-8") as input_file:
        with open(output_path, "w") as output_file:
            output_file.write(input_file.read())

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: python input-file.xppp [output-file.xml]")
        exit()

    input_path: str = sys.argv[1]
    
    # The second argument is optional, if it insn't given take the filename of
    # the first argument and add "".xml"
    if len(sys.argv) == 2: output_path: str = sys.argv[1].split(".")[0] + ".xml"
    else: output_path: str = sys.argv[2]
    
    xopp2xml(input_path, output_path)


if __name__ == "__main__":
    main()