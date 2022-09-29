import sys # for command-line arguments
import os # for file system

def png2longpng(png_paths: list[str], output_path):
    import pygame # for image manipulation
    pygame.init()

    img_surfaces: list[pygame.Surface] = []
    # this will be the width of the most wide image at the end of the loop
    max_width: int = 0 
    # all heights all added up
    height: int = 0
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
        max_width = max(surf.get_width(), max_width)
        height += surf.get_height()

    # The long transparent image (as a pygame surface)
    long_img: pygame.Surface = pygame.Surface((max_width, height), 
                                                        pygame.SRCALPHA)
    MIDDLE_X: int = round(max_width/2)
    current_height: int = 0
    for surf in img_surfaces:
        # top left will be the blitting position, but the image should be 
        # centered anyway
        blit_pos = (MIDDLE_X - round(surf.get_width()/2), current_height)
        long_img.blit(surf, blit_pos)
        current_height += surf.get_height()

    # saving the file to the specified file
    pygame.image.save(long_img, output_path)
    print(f"Saved image file to '{output_path}'")


def main():
    if len(sys.argv) < 3:
        print("""Usage:
    All image files as single arguments:
        python imgs2longimg.py output-file input-file1 input-file2 [input-file3, ...]

    Use all image files inside of a folder:
        python imgs2longimg.py output-file -d input-directory
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