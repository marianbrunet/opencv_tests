
import numpy as np
import cv2 as cv
import sys, getopt

def fix_blemish(image, source_pos, target_pos, radius):
	#Copy original 
    imagecopy = image.copy()
	# Select the region
    spot = imagecopy[source_pos[1]-radius:source_pos[1]+radius, source_pos[0]-radius:source_pos[0]+radius]
    removal = np.ones(spot.shape, spot.dtype) * 255
    #use all pixels same color as a boundary pixel
    removal = (imagecopy[source_pos[1]+radius, source_pos[0]+radius])*removal
    # Get a mask for the region
    spotmask = np.ones(spot.shape, spot.dtype) * 255
	# Feather mask
    spotmask = cv.GaussianBlur(spotmask, (5,5), 0, 0)

	# Return the clone of image, mask
    fix = cv.seamlessClone(removal, imagecopy, spotmask, target_pos, cv.NORMAL_CLONE)
    return fix


# Define brush size
brush_size = 15

def on_mouse(event, x, y, flags, userdata):
    global target, image_input
    mouse_pos = (x, y)
    # User will click to select the target region that will be replaced. 
    if event == cv.EVENT_LBUTTONDOWN:
        target = mouse_pos
        fixed = fix_blemish(image_input, (target[0]+8, target[1]+8), target, 15)
        image_input = fixed
        cv.imshow("fixed", image_input)

# Read image in color mode
filename = "blemish.png"
img = cv.imread(filename, cv.IMREAD_COLOR)

# If image is not read properly, return error
if img is None:
    print('Failed to load image file: {}'.format(filename))

# Create a copy of original image
img_mask = img.copy()
global image_input
image_input = img_mask
global target

# Create a display window
window_name = "Blemish Fix"
cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
cv.imshow(window_name, image_input)
cv.setMouseCallback(window_name, on_mouse)


while True:
    ch = cv.waitKey()
    if ch == 27:
        break
    else:
        pass
       

cv.destroyAllWindows()