import sys # for command-line arguments
import gzip # for unzipping gzipped files
import os # for file system

def xml2xopp(input_path: str, output_path: str):
    with open(input_path, "r") as input_file:
        with gzip.open(output_path, "wt", encoding="utf-8") as output_file:
            output_file.write(input_file.read())

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("Usage: python input-file.xml [output-file.xopp]")
        exit()

    input_path: str = sys.argv[1]
    
    # The second argument is optional, if it insn't given take the filename of
    # the first argument and add "".xopp"
    if len(sys.argv) == 2: output_path: str = sys.argv[1].split(".")[0] + ".xopp"
    else: output_path: str = sys.argv[2]
    
    xml2xopp(input_path, output_path)


if __name__ == "__main__":
    main()