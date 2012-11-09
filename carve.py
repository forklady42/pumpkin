import Image
import numpy as np
from math import fabs


@profile
def gradient(im):
    
    r, g, b = np.array(im).T
            
    xgrad = np.transpose(np.gradient(r)[0]+np.gradient(g)[0]+np.gradient(b)[0])
    ygrad = np.transpose(np.gradient(r)[1]+np.gradient(g)[1]+np.gradient(b)[1])
    
    return xgrad, ygrad
    
def v_seam(x_array, y_array):
    
    memo_array = np.zeros(shape=(x_array.shape))
    pointer_array = np.zeros(shape=(x_array.shape))
    
    for a in range(x_array.shape[1]):
        memo_array[0, a] = (fabs(x_array[0, a]) + fabs(y_array[0, a]))**2
    
    (row, pixel) = x_array.shape
    
    
    for i in range(1, row):
        for j in range(pixel):
            grad = (fabs(x_array[i, j]) + fabs(y_array[i, j]))**2
            
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
        trav = [row-2-i, trav[1]+b]
                
    return seam_array
    
def h_seam(x_array, y_array):
    
    a = v_seam(np.transpose(x_array), np.transpose(y_array))
    
    return np.transpose(a)
    
    
def vdelete_seam(im, sarray):
    
    pixels = im.load()
    
    width, height = im.size[0], im.size[1]
    
    new_im = Image.new('RGB', (width-1, height))
    pixels_new = new_im.load()
    
    for y in range(height):
        removed = 0
        for x in range(width):
            if sarray[y, x]:
                removed += 1
            else:
                pixels_new[x-removed, y] = pixels[x, y]
                
    return new_im
    
def hdelete_seam(im, sarray):
    
    pixels = im.load()
    
    width, height = im.size[0], im.size[1]
    
    new_im = Image.new('RGB', (width, height-1))
    pixels_new = new_im.load()
    
    for x in range(width):
        removed = 0
        for y in range(height):
            if sarray[y, x]:
                removed += 1
            else:
                pixels_new[x, y-removed] = pixels[x, y]
                
    return new_im
    
@profile
def carve(file, ratio):
    im = Image.open(file)
    
    wd_rm = 0
    ht_rm = 0
    
    im_ratio = float(im.size[0])/im.size[1]
        
    if ratio < im_ratio:
        wd_rm = im.size[0] - int(ratio*im.size[1])
    else:   # The equals to is fine as it should evaluate to zero below
        ht_rm = im.size[1] - int(1/ratio*im.size[0])
    
    for i in range(wd_rm):
        [x_array, y_array] = gradient(im)
        sarray = v_seam(x_array, y_array)
        im = vdelete_seam(im, sarray)
        
    for i in range(ht_rm):
        [x_array, y_array] = gradient(im)
        sarray = h_seam(x_array, y_array)
        im = hdelete_seam(im, sarray)
    
    im.show()
    
if __name__ == "__main__":
    #f = raw_input("File: ")
    #ratio = raw_input("Aspect ratio (enter as x:y): ")
    
    #[x, y] = map(lambda a: float(a), ratio.split(":"))
    
    #carve(f, x/y)
    carve("shelf.jpg", 3.5/5.0)