import Image
import numpy as np
from math import fabs


def gradient(im):
    
    im_grey = im.convert("F")
    
    #what if try with rgb instead of grey?
    blah = np.transpose(np.array(im_grey.getdata()).reshape(im_grey.size[0], im_grey.size[1]))    
    x,y=np.gradient(blah)
    
    #Laplacian:
    return np.gradient(x)[0], np.gradient(y)[1]
    
    #return np.gradient(blah)
    
#def sobel():
    
def v_seam(x_array, y_array):
    
    memo_array = np.zeros(shape=(x_array.shape))
    pointer_array = np.zeros(shape=(x_array.shape))
    
    for a in range(x_array.shape[1]):
        memo_array[0, a] = fabs(x_array[0, a]) + fabs(y_array[0, a])
    
    (row, pixel) = x_array.shape
    
    
    for i in range(1, row):
        for j in range(pixel):
            grad = fabs(x_array[i, j]) + fabs(y_array[i, j])
            
            if (j < (pixel-1)) and (j != 0):
                
                a = memo_array[i-1, j-1]
                b = memo_array[i-1, j]
                c = memo_array[i-1, j+1]
                
                if a < b and a < c:
                    path = a
                    point = -1
                elif c < b:
                    path = c
                    point = 1
                else:
                    path = b
                    point = 0
                
            elif j == (pixel-1):
                a = memo_array[i-1, j-1]
                b = memo_array[i-1,   j]
                
                if a < b:
                    path = a
                    point = -1
                else:
                    path = b
                    point = 0
            else:
                a = memo_array[i-1, j+1]
                b = memo_array[i-1, j]
                
                if a < b:
                    path = a
                    point = 1
                else:
                    path = b
                    point = 0
            memo_array[i, j] = grad + path
            pointer_array[i, j] = point
    
    seam_array = np.zeros(shape=(x_array.shape))
    
    mindex = memo_array.argmin(axis=1)[row-1]
    
    trav = [(row-1), mindex]
    for i in range(row):
        seam_array[trav[0], trav[1]] = 1
        b = pointer_array[trav[0], trav[1]]
        #print memo_array[trav[0], trav[1]]
        trav = [row-2-i, trav[1]+b]
                
    return seam_array
    
def h_seam(x_array, y_array):
    
    a = v_seam(np.transpose(x_array), np.transpose(y_array))
    
    return np.transpose(a)
    
    
def vdelete_seam(im):
    
    pixels = im.load()

    [x_array, y_array] = gradient(im)
    #grad_array = x_array + y_array
    
    sarray = v_seam(x_array, y_array)
    
    width, height = im.size[0], im.size[1]
    
    new_im = Image.new('RGB', (width-1, height))
    #new_im = Image.new('RGB', (width, height))
    pixels_new = new_im.load()
    
    for y in range(height):
        removed = 0
        for x in range(width):
            if sarray[y, x]:
                #pixels_new[x, y] = (0, 100, 0)
                if removed >= 1:
                    print "Alert!"
                removed += 1
            else:
                pixels_new[x-removed, y] = pixels[x, y]
                #pixels_new[x, y] = pixels[x,y]
                
    #pixels_new[0, 39] = (0,100,0)
    return new_im
    
def hdelete_seam(im):
    
    pixels = im.load()

    [x_array, y_array] = gradient(im)
    
    sarray = h_seam(x_array, y_array)
    
    width, height = im.size[0], im.size[1]
    
    new_im = Image.new('RGB', (width, height-1))
    #new_im = Image.new('RGB', (width, height))
    pixels_new = new_im.load()
    
    for x in range(width):
        removed = 0
        for y in range(height):
            if sarray[y, x]:
                #pixels_new[x, y] = (0, 100, 0)
                if removed >= 1:
                    print "Alert!"
                removed += 1
            else:
                pixels_new[x, y-removed] = pixels[x, y]
                #pixels_new[x, y] = pixels[x,y]
                
    return new_im

def main(wd_rm, ht_rm):
    im = Image.open("sand.jpg")
    
    for i in range(wd_rm):
        im = vdelete_seam(im)
        
    for i in range(ht_rm):
        im = hdelete_seam(im)
    
    im.show()

if __name__ == "__main__":
    main(0, 100)