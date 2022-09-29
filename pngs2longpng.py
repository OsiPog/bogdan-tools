import sys # for command-line arguments
import os # for file system

def png2longpng(png_paths: list[str], output_path):
    import pygame # for image manipulation
    print(png_paths, output_path)


def main():
    if len(sys.argv) < 3:
        print("""Usage:
    All image files as single arguments:
        python png2longpng.py output-file input-file1 input-file2 [input-file3, ...]

    Use all image files inside of a folder:
        python png2longpng.py output-file -d input-directory
""")
        exit()

    output_path: str = sys.argv[1]

    # Normally every file should be given as an argument
    png_paths: list[str] = sys.argv[2:]
    
    # you can also give a folder with images
    if "-d" in sys.argv:
        png_paths = os.listdir(sys.argv[2:])

    png2longpng(png_paths, output_path)


if __name__ == "__main__":
    main()