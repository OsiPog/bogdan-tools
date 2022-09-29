import sys # for command-line arguments
import os # for file system

class OnlyNotEnoughImagesError(Exception):
    pass

def png2longpng(png_paths: list[str], output_path, max_height=None, 
                max_width=None):
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
    MIDDLE_X: int = round(long_width/2)
    current_height: int = 0
    for surf in img_surfaces:
        # top left will be the blitting position, but the image should be 
        # centered anyway
        blit_pos = (MIDDLE_X - round(surf.get_width()/2), current_height)
        long_img.blit(surf, blit_pos)
        current_height += surf.get_height()

    # scaling long image according to max_height or max_width


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
        -h\tScaling the image down to a certain height if it exceeds it
        -w\tScaling the image down to a certain width if it exceeds it
        \t(if both options are enabled be aware that the image may be stretched)
        -bg\tAdds a background colour to the output image

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

    png2longpng(png_paths, output_path)


if __name__ == "__main__":
    main()