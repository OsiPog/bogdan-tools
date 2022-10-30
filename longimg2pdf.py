import sys # for command-line arguments
import os # for file system
import PIL # for image manipulation
from PIL import Image

def element_after(element, arr: list, convert_to=None):
    """Returns the next element after the given element in the provided list.

    Args:
        arr (list): list which should be searched through
        element (any): the element before the wanted element in the list.
        convert_to (any): converts the result to some data-type.

    Returns:
        Any: Depends on the datatype of the element. 
        NoneType: If the given element isn't in the list or is the last element.
    """
    result = None
    try: result = arr[arr.index(element)+1]
    except ValueError: pass
    
    try:
        if convert_to is not None: result = convert_to(result)
    except TypeError: pass
        
    return result

def longimg2pdf():
    pass

def main():
    if len(sys.argv) < 3:
        print("""Usage: python longimg2pdf.py output-file.pdf input-file [options]
    Options:
        -asp <float>\tThe aspect ratio (width/height) of every pdf page 
                    \t(default: 0.70707, DIN A4)
""")
        exit()

    # Argument positions as stated in the help message.
    output_path: str = sys.argv[1]
    img_path: list[str] = sys.argv[2]

    
    longimg2pdf(img_path, output_path,
                aspect_ratio = element_after("-asp", sys.argv, float))


if __name__ == "__main__":
    main()