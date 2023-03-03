# bogdan-tools

This repository contains scripts I used in my [Bogdan](https://github.com/OsiPog/bogdan) (abandoned) project. These scripts are quite modular so feel free to use them yourself.



## imgs2longimg.py

A command-line tool to convert multiple images to one long image.

### Demonstration

![](https://i.imgur.com/rxEpWFX.png)

### Usage

`python imgs2longimg.py <arguments> [options]`

- Arguments

  - All image files as single arguments:

     `output-file input-file1 input-file2 [input-file3, ...] [options]`

  - Use all image files inside a folder:

    `output-file -d input-directory [options]`

- Options:

  `-h <int>`    Scaling the image down to a certain height if it exceeds it.

  `-w <int>`    Scaling the image down to a certain width if it exceeds it.

  `-bg <hex>`  Adds a background colour to the output image (e. g. '#FFFFFF' for white).
