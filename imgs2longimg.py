import sys # for command-line arguments
import os # for file system
import PIL # for image manipulation
from PIL import Image

# Custom Exceptions
class OnlyNotEnoughImagesError(Exception):
    TEXT = "A long image can only consist of 2 images or more."
    pass
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

def imgs2longimg(png_paths: list[str], output_path: str, max_width: int=None, 
                max_height: int=None, background: str=None, 
                bypass_not_enough: bool = False):
    """Connecting multiple images to one long image.

    Args:
        png_paths (list[str]): A list of all input-image paths.
        output_path (str): The file path of the long output-image.
        max_width (int, optional): Scale the image down if value exceeded.
        max_height (int, optional): Scale the image down if value exceeded.
        background (str, optional): Add a background colour to the image.

    Raises:
        OnlyNotEnoughImagesError: If less than 2 input-images are provided.
        WrongColourFormat: If anything else but '#FFFFFF' is used as background.
    """

    if (len(png_paths) < 2) and not bypass_not_enough: 
        raise OnlyNotEnoughImagesError(OnlyNotEnoughImagesError.TEXT)


    pil_images: list = []
    # this will be the width of the most wide image at the end of the loop
    long_width: int = 0 
    # all heights all added up
    long_height: int = 0
    for png_path in png_paths:
        try:
            image = Image.open(png_path, "r")

            # Error would happen one line above
            print(f"successfully loaded '{png_path}'.")
        
        except PIL.UnidentifiedImageError: 
            print(f"failed loading of '{png_path}'. skipping it")
            continue
        
        pil_images.append(image)
        long_width = max(image.size[0], long_width)
        long_height += image.size[1]

    # if a background is specified get it
    color = (0, 0, 0, 0)
    if background: 
        color = hex_color_to_tuple(background, alpha=255)

    # The long transparent image (as a pygame surface)
    long_image = Image.new("RGBA", (long_width, long_height), color)
    
    MIDDLE_X: int = round(long_width/2)
    current_height: int = 0
    for image in pil_images:
        # getting the right offset so that the images are centered and above
        # each other
        paste_offset = (MIDDLE_X - round(image.size[0]/2), current_height)
        
        # This is faster than alpha_composite but has an unwanted side effect
        # when using a background colour and an image with alpha pixels, 
        # I personally won't have images with alpha pixels inside so I chose 
        # speed here.
        long_image.paste(image, paste_offset)
        
        current_height += image.size[1]

    # scaling long image according to max_height or max_width
    if not max_width: max_width = long_image.size[0]
    if not max_height: max_height = long_image.size[1]
    long_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # saving the file to the specified file
    long_image.save(output_path)
    print(f"Saved image file to '{output_path}'")


def main():
    if len(sys.argv) < 3:
        print("""Usage: python imgs2longimg.py <arguments> [options]
    Arguments:
        All image files as single arguments:
            output-file input-file1 input-file2 [input-file3, ...] [options]

        Use all image files inside a folder:
            output-file -d input-directory [options]

    Options:
        -h <int>\tScaling the image down to a certain height if it exceeds it
        -w <int>\tScaling the image down to a certain width if it exceeds it
        -bg <hex>\tAdds a background colour to the output image (e. g. '#FFFFFF' for white)
""")
        exit()

    output_path: str = sys.argv[1]

    # Normally every file should be given as an argument
    png_paths: list[str] = sys.argv[2:]
    
    # you can also give a folder with images
    if sys.argv[2] == "-d":
        png_paths.clear()
        folder = sys.argv[3]
        for file in os.listdir(folder):
            png_paths.append(f"{folder}/{file}")

    imgs2longimg(png_paths, output_path, 
                 max_width = element_after("-w", sys.argv, int), 
                 max_height = element_after("-h", sys.argv, int), 
                 background = element_after("-bg", sys.argv))


if __name__ == "__main__":
    main()