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

def longimg2pdf(input_path: str, output_path: str, aspect_ratio: float = None,
                bg_color: str=None):
    if aspect_ratio is None: aspect_ratio = 0.70707 # DIN A4 paper format
    if bg_color is None: bg_color = "#FFFFFF" # white
    
    long_image = Image.open(input_path)

    
    page_height: int = int(long_image.width/aspect_ratio)
    page_amount: int = int(long_image.height/page_height)

    pil_images: list = []
    for i in range(page_amount+1):
        y0 = i*page_height
        y1 = y0 + page_height
        
        # if it's the last image, set the second y value to the end of the 
        # image (just in case)
        if i == page_amount: y1 = long_image.height
        
        # creating the background (A pdf cannot be transparent)
        background= Image.new("RGBA", (long_image.width, y1-y0), 
                             hex_color_to_tuple(bg_color))
        # cropping the page out of the long image
        cropped = long_image.crop((0, y0, long_image.width, y1))
        
        # paste the cropped image onto the background
        background.alpha_composite(cropped, 
                                   (int(background.width/2-cropped.width/2),0))
        # Append the background image (with the cropped image on top) 
        # to the list
        pil_images.append(background.convert("RGB"))
    
    # Save the images (pages) to a pdf file
    pil_images[0].save(output_path, "PDF", resolution=100.0, save_all=True,
                       append_images=pil_images[1:])

def main():
    if not (2 <= len(sys.argv) <= 3):
        print("""Usage: python input-file output-file.pdf [options]

    Options:
        -asp <float>    define the aspect ratio of every page (default: 0.707 (DIN A4)).
        -bg <hex>       set a custom background colour (default is white, format: #FFFFFF)
""")
        exit()

    input_path: str = sys.argv[1]
    output_path: str = sys.argv[2]
    
    longimg2pdf(input_path, output_path, 
                aspect_ratio=element_after("-asp", sys.argv),
                bg_color=element_after("-bg", sys.argv))


if __name__ == "__main__":
    main()