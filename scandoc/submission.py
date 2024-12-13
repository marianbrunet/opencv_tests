# Enter your code here
#%%
import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread('scanned-form.jpg')
mask = np.zeros(image.shape[:2], np.uint8)
width = image.shape[1]
height = image.shape[0]

# Define the bounding rectangle for the object of interest
rect = (20, 150, image.shape[1]-20, image.shape[0]-20)  # (x, y, width, height)
# background and foreground models
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

#%%
#1 Use GrabCut-------------------------------------------------------
# specify the background and foreground model, background is dark
backgroundModel = np.zeros((1, 65), np.float64)
foregroundModel = np.zeros((1, 65), np.float64)
# Apply GrabCut algorithm
cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
# Create a binary mask from the GrabCut result
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
# Multiply the image with the binary mask to get the segmented object.
result = image * mask2[:, :, np.newaxis]

#%%
#2 findContour-----------------------------------------------------
# Detect edges
image_copy = result.copy()
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 2)
# Show the image
#cv2.imshow('Contours', image_copy)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#%%
#3 approxPolyDP -----------------------------------------------------
# Contour of the edges, use approxPolyDP
image_ctr = image.copy()
cnts = contours
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

for c in cnts:
    perim = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * perim, True)

    if len(approx) == 4:
        screenCnt = approx
        print("found outline!")
        break

# Display
# cv2.drawContours(image_ctr, [screenCnt], -1, (0, 255, 0), 2)
# cv2.imshow("Outline", image_ctr)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#%% 4 transform perspective
width = image.shape[1]
height = image.shape[0]
#organize points to match
organized = [screenCnt[1][0], screenCnt[0][0], screenCnt[2][0], screenCnt[3][0]]
#desdired width 500px
A = 500/width

pts1 = np.float32(organized)
pts2 = np.float32([[0, 0], [int(A*width), 0],
                       [0, int(A*height)], [int(A*width), int(A*height)]])


M = cv2.getPerspectiveTransform(pts1, pts2);
warped = cv2.warpPerspective(image_ctr, M, (int(A*width), int(A*height)))

cv2.imshow("Original", image)
cv2.imshow("Scanned", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()


# %%
