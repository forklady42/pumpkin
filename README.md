Pumpkin
====

A seam carver implementation for [content aware image scaling] (http://www.faculty.idc.ac.il/arik/SCWeb/imret/imret.pdf).

##Usage

    $ python carve.py

will ask for the file path to the original image and the desired aspect ratio entered as width:height. 
Alternatively, `import carve` and directly call `carve(file, ratio)`. (Note: in the second case, ratio should be a float.)

##Example

Height and width reductions using this implementation:

<img src='http://betsy-cannon.com/images/seam_carving.jpg'/>


##Limitations
Currently, this implementation changes aspect ratio only by removing pixels, thereby, 
reducing the size of the image. In the future, support will be added for expanding the  
image as well.

In general, seam carving does not handle content dense images well, as there are no low energy seams to remove.