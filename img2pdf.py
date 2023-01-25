import sys # for command-line arguments
import os # for file system
import PIL # for image manipulation
from PIL import Image

# Custom Exceptions
class WrongColourFormat(Exception):
    TEXT = "{} is not in the right format, please use hexadecimal from '#000000' to '#FFFFFF' and don't forget the leading '#'."
    pass

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

def hex_color_to_tuple(hex_: str, alpha: int=None):
    if (len(hex_) != 7) or (hex_[0] != "#"): raise WrongColourFormat(
        WrongColourFormat.TEXT.format(hex_))

    try:
        r: int = int(hex_[1:3], 16)
        b: int = int(hex_[3:5], 16)
        g: int = int(hex_[5:], 16)
    except ValueError: raise WrongColourFormat(
        WrongColourFormat.TEXT.format(hex_))
    
    if alpha: return (r, g, b, alpha)
    else: return (r, g, b)

def img2pdf(input_path: str, output_path: str, bg_color: str=None,
            max_width: int=None, max_height: int=None,
            fast_mode: bool = False):
    if bg_color is None: bg_color = "#FFFFFF" # white
    
    image = Image.open(input_path)
    
    if not fast_mode:
        image = image.convert("RGBA")

    background = Image.new("RGB", image.size, hex_color_to_tuple(bg_color))

    if fast_mode:
        background.paste(image, (0,0))
    else:
        background.convert("RGBA").alpha_composite(image, (0,0))
        background = background.convert("RBG")

    # scaling the image according to max_height or max_width
    if not max_width: max_width = background.size[0]
    if not max_height: max_height = background.size[1]
    background.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    background.save(output_path, "PDF", resolution=100.0)

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("""Usage: python input-file output-file.pdf
              
    Options:
        -bg <hex>   Sets the background colour (Defaults to white, #FFFFFF)
""")
        exit()

    input_path: str = sys.argv[1]
    output_path: str = sys.argv[2]
    
    img2pdf(input_path, output_path, bg_color=element_after("-bg", sys.argv))


if __name__ == "__main__":
    main()