import sys # for command-line arguments
import os # for file system
from PyPDF2 import PdfReader # to get pdf page size and count
import xml.etree.ElementTree as gfg # for xml creation
import gzip # gzipping .xml to .xopp

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

def pdf2xopp(pdf_path: str, output_path: str, pdf_path_in_xopp: str=None):
    # If no special path for the xopp file is given, take the available pdf 
    # path.
    if pdf_path_in_xopp is None: pdf_path_in_xopp = pdf_path
    
    # Create the xml and the default hardcoded header
    root = gfg.Element("xournal")
    root.set("creator", "Xournal++ 1.1.1")
    root.set("fileversion", "4")
    
    # Take the pdf apart and expand the xml in the meantime.
    pdf = PdfReader(pdf_path)
    
    for i,page in enumerate(pdf.pages):
        # Determine the page size
        xopp_page_height: float = 841.889764 # Value taken from a default xopp document
        xopp_page_width: float = xopp_page_height * float(page.mediabox[2]/page.mediabox[3])
        
        page_xml = gfg.SubElement(root, "page")
        page_xml.set("width", str(xopp_page_width))
        page_xml.set("height", str(xopp_page_height))
        
        bg_xml = gfg.SubElement(page_xml, "background")
        bg_xml.set("type", "pdf")
        # These attributes are only needed on the first page
        if i == 0:
            bg_xml.set("domain", "absolute")
            bg_xml.set("filename", pdf_path_in_xopp)
        bg_xml.set("pageno", str(i+1))
    
    # Saving the xml file gzipped with the extension xopp
    tree = gfg.ElementTree(root) # An element tree that can write bytes to files
    with gzip.open(output_path, "wb") as output_file:
        tree.write(output_file)
    
        
    
    
    
    
    
    
    
def main():
    if len(sys.argv) < 3:
        print("""Usage: python longimg2pdf.py output-file.xopp input-file [options]

    Options:
        -p <str>    Defines which path to the pdf should be put into the xopp file.
""")
        exit()

    # Argument positions as stated in the help message.
    pdf_path: str = sys.argv[1]
    xopp_path: str = sys.argv[2]

    pdf2xopp(pdf_path, xopp_path, 
             pdf_path_in_xopp=element_after("-p", sys.argv))


if __name__ == "__main__":
    main()