#!/usr/bin/env python
# coding: utf-8

#%%
import cv2
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 10.0)
matplotlib.rcParams['image.cmap'] = 'gray'


#%%
def cartoonify(image, arguments=0):

    # first convert image to grayscale
    grayImage= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #apply median blur
    MB_grayImage = cv2.medianBlur(grayImage, 5)
    plt.imshow(MB_grayImage, cmap='gray'); plt.show();

    # retrieve the edges for the cartoon effect
    edges1 = cv2.Canny(MB_grayImage,10,200)
    edges2 = cv2.adaptiveThreshold(MB_grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    edges = edges1 + edges2
    plt.imshow(edges, cmap='gray'); plt.show();
    
    #applying bilateral to color image to remove noise
    # We need to keep sharp edges -> bilateral
    colorImage = cv2.bilateralFilter(image, 12, 400, 400)
    plt.imshow(cv2.cvtColor(colorImage, cv2.COLOR_BGR2RGB)); plt.show();

    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edges)
    cartoonImage = cv2.cvtColor(cartoonImage, cv2.COLOR_BGR2RGB)
    plt.imshow(cartoonImage); plt.show();

    cartoonImage = cv2.cvtColor(cartoonImage, cv2.COLOR_BGR2RGB)
    return cartoonImage

#%%
def pencilSketch(image, arguments=0):
    
    ### YOUR CODE HERE
    # Convert to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(image_gray, cmap='gray'); plt.show();
    # Inversion
    image_invert = cv2.bitwise_not(image_gray)
    plt.imshow(image_invert, cmap='gray'); plt.show();

    #get a smooth version and subtract it from the original
    image_smooth = cv2.GaussianBlur(image_invert, (15, 15), sigmaX=0, sigmaY=0)
    plt.imshow(image_smooth, cmap='gray'); plt.show();

    result = cv2.divide(image_gray, 255 - image_smooth, scale=256)
    plt.imshow(result, cmap='gray'); plt.show();
    pencilSketchImage = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    return pencilSketchImage


#%%
imagePath = "pizza.jpg"
image = cv2.imread(imagePath)

cartoonImage = cartoonify(image)
pencilSketchImage = pencilSketch(image)

#%%
plt.figure(figsize=[20,10])
plt.subplot(131);plt.imshow(image[:,:,::-1]);
plt.subplot(132);plt.imshow(cartoonImage[:,:,::-1]);
plt.subplot(133);plt.imshow(pencilSketchImage[:,:,::-1]);
# %%
#