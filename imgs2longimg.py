import sys # for command-line arguments
import os # for file system

# Custom Exceptions
class OnlyNotEnoughImagesError(Exception):
    pass
class WrongColourFormat(Exception):
    pass

def imgs2longimg(png_paths: list[str], output_path: str, max_width: int=None, 
                max_height: int=None, background: str=None):
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
    if len(png_paths) < 2: raise OnlyNotEnoughImagesError(
        "A long image can only be made out of 2 images or more.")

    # initialising pygame for image manipulation
    import pygame
    pygame.init()

    img_surfaces: list[pygame.Surface] = []
    # this will be the width of the most wide image at the end of the loop
    long_width: int = 0 
    # all heights all added up
    long_height: int = 0
    for png_path in png_paths:
        try:
            surf = pygame.image.load(png_path)

            # Error would happen one line above
            print(f"successfully loaded '{png_path}'.")
        
        # Thank you pygame for providing such a specific exception type
        except pygame.error: 
            print(f"failed loading of '{png_path}'. skipping it")
            continue
        
        img_surfaces.append(surf)
        long_width = max(surf.get_width(), long_width)
        long_height += surf.get_height()

    # The long transparent image (as a pygame surface)
    long_img: pygame.Surface = pygame.Surface((long_width, long_height), 
                                                        pygame.SRCALPHA)
    
    # if background specified, fill it with it
    if background:
        try:
            color = pygame.Color(background)
        except ValueError: 
            raise WrongColourFormat(
            f"'{background}' is not in the right format, please use hexadecimal from '#000000' to '#FFFFFF' and don't forget the leading '#'.")
        # Adding the background colour
        long_img.fill(color)
    
    MIDDLE_X: int = round(long_width/2)
    current_height: int = 0
    for surf in img_surfaces:
        # top left will be the blitting position, but the image should be 
        # centered anyway
        blit_pos = (MIDDLE_X - round(surf.get_width()/2), current_height)
        long_img.blit(surf, blit_pos)
        current_height += surf.get_height()

    # scaling long image according to max_height or max_width
    if max_width:
        width = long_img.get_width()
        if max_width < width:
            ratio = max_width/width  
            long_img = pygame.transform.scale(long_img, (max_width, 
                                               round(long_img.get_height()*ratio)))
    if max_height:
        height = long_img.get_height()
        if max_height < height:
            ratio = max_height/height 
            long_img = pygame.transform.scale(long_img, (round(long_img.get_width()*ratio),
                                               max_height))

    # saving the file to the specified file
    pygame.image.save(long_img, output_path)
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

    # Checking for any options
    
    # initialising variable
    max_width: int = None
    # if exists convert to int and take value of index after option indicator
    try: max_width = int(sys.argv[sys.argv.index("-w")+1])
    except ValueError: pass
    
    max_height: int = None
    try: max_height = int(sys.argv[sys.argv.index("-h")+1])
    except ValueError: pass
    
    background: int = None
    try: background = sys.argv[sys.argv.index("-bg")+1]
    except ValueError: pass
    print(output_path, max_width, max_height, background)
    imgs2longimg(png_paths, output_path, max_width, max_height, background)


if __name__ == "__main__":
    main()