import sys
import xml.etree.ElementTree as gfg # for xml creation
import gzip # gzipping .xml to .xopp
import PIL # for image manipulation
from PIL import Image
from pdf2image import convert_from_path # pillow doesnt support reading pdf
import base64 # base 64 encoding
from io import BytesIO # byte array

def pdf2xopp(pdf_path: str, xopp_path: str, poppler_path: str = None, 
             max_width: int = None, max_height: int = None):
    
    # default hardcoded header
    root = gfg.Element("xournal")
    root.set("creator", "Xournal++ 1.1.1")
    root.set("fileversion", "4")
    print("initilised xml for xopp")
    
    # Convert the pdf to PIL images
    pil_pdf_images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    for i,page in enumerate(pil_pdf_images):
        # Determine the page size (to keep the aspect ratio)
        xopp_page_width: float = 595.27559100 # default from xopp document
        xopp_page_height: float = xopp_page_width * float(page.size[1]/page.size[0])
        
        page_xml = gfg.SubElement(root, "page")
        page_xml.set("width", str(xopp_page_width))
        page_xml.set("height", str(xopp_page_height))

        # set a background (checked paper)
        bg_xml = gfg.SubElement(page_xml, "background")
        bg_xml.set("type", "solid")
        bg_xml.set("color", "#ffffffff")
        bg_xml.set("style", "graph")
        
        # The image element is wrapped by a layer element
        layer_xml = gfg.SubElement(page_xml, "layer")
        
        img_xml = gfg.SubElement(layer_xml, "image")
        # That it fills the whole page (will not be strechted)
        img_xml.set("left", "0")
        img_xml.set("top", "0")
        img_xml.set("right", str(xopp_page_width))
        img_xml.set("bottom", str(xopp_page_height))
        
        # convert the current page to a base 64 encoded PNG image
        
        # downscale the image to a given maximum
        if not max_width: max_width = page.size[0]
        if not max_height: max_height = page.size[1]
        page.thumbnail((max_width, max_height))
        
        bytes_buffer = BytesIO()
        page.save(bytes_buffer, format="PNG")
        img_xml.text = base64.b64encode(bytes_buffer.getvalue()).decode()

    
    # Saving the xml file gzipped with the extension xopp
    tree = gfg.ElementTree(root) # An element tree that can write bytes to files
    with gzip.open(xopp_path, "wb") as output_file:
        tree.write(output_file)
        
        
def main():
    if len(sys.argv) < 3:
        print("""Usage: python pdf2xopp.py output-file.xopp input-file.pdf [options]""")
        exit()

    # Argument positions as stated in the help message.
    pdf_path: str = sys.argv[2]
    xopp_path: str = sys.argv[1]

    pdf2xopp(pdf_path, xopp_path)


if __name__ == "__main__":
    main()