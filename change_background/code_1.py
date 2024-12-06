import cv2 as cv
import numpy as np

video = cv.VideoCapture("greenscreen-demo.mp4")
background = cv.imread("background.jpg")


#First select patch of green
# Callback function to capture color on mouse click
def pick_color(event, x, y, flags, param):
    global selected_color
    if event == cv.EVENT_LBUTTONDOWN:
        # Get the color at the clicked pixel
        color_bgr = image[y, x]
        selected_color = color_bgr
        print(f"Clicked Color (BGR): {color_bgr}")
        
def updateFiltering(*args):
    global scaleFactor
    scaleFactor = (int) (args[0])


# Load the image
ret, frame = video.read()
frame = cv.resize(frame, (640, 480))
#image = # Convert the image to HSV color space
image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


cv.namedWindow('Image')
cv.setMouseCallback('Image', pick_color)

print("Click on the image to select a color. Press 'q' to exit.")
# Display the image and wait for user interaction
while True:
    cv.imshow('Image', frame)
    key = cv.waitKey(1)
    if key == ord('q'):  # Exit the loop on pressing 'q'
        break

cv.destroyAllWindows()

h = selected_color[0]
s = selected_color[1]
v = selected_color[2]

#Add track bar
maxScaleUp = 50
global scaleFactor
scaleFactor = 1

windowName = "Remove Background"
trackbarValue = "Sensitivity"
# Create a window to display results
cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)
cv.createTrackbar(trackbarValue, windowName, scaleFactor, maxScaleUp, updateFiltering)


# Now do background removal
while True:

    ret, frame = video.read()

    frame = cv.resize(frame, (640, 480))
    image = cv.resize(background, (640, 480))

    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    #print('selected color: ', b, g, r)

    l_green = np.array([h-scaleFactor, 50, 50])
    u_green = np.array([h+scaleFactor, 255, 255])

    mask = cv.inRange(frame, l_green, u_green)
    cv.imshow("maskq", mask)

    # Invert the mask to keep non-green areas
    mask_inv = cv.bitwise_not(mask)

    # Apply the mask to make green areas transparent
    #frame[:, :, 3] = mask_inv

    #imageF = cv.addWeighted(frame, 1, background, 1, 0)
    cv.imshow("maskqF", mask_inv)
    res = cv.bitwise_and(frame, frame, mask = mask_inv)
    f = frame - res
    f = np.where(f == 0, frame, image)
    

    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
    f = cv.cvtColor(f, cv.COLOR_HSV2BGR)


    cv.imshow("original", frame)
    cv.imshow(windowName, f)

    if cv.waitKey(25) == 27:
        break 


video.release()
cv.destroyAllWindows()