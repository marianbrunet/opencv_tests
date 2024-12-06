#%%
import cv2
import math

# Lists to store the points
top_left=[]
bottom_right=[]

#%%
def drawRectangle(action, x, y, flags, userdata):
  # Referencing global variables 
  global top_left, bottom_right
  # Action to be taken when left mouse button is pressed
  if action==cv2.EVENT_LBUTTONDOWN:
    top_left=[(x,y)]
    # Mark the top left corner
    cv2.circle(source, top_left[0], 1, (255,0,255), 2, cv2.LINE_AA );

    # Action to be taken when left mouse button is released
  elif action==cv2.EVENT_LBUTTONUP:
    bottom_right=[(x,y)]
    # Mark the bottom right left corner
    cv2.circle(source, bottom_right[0], 1, (255,0,255), 2, cv2.LINE_AA );

    # Draw the rectangle
    cv2.rectangle(source, top_left[0], bottom_right[0], (255,0,255),2, cv2.LINE_AA)
    cv2.imshow("Window",source)

    #Now also save the cropped image from this rectangle
    cropped_source = source[top_left[0][1]:bottom_right[0][1], top_left[0][0]:bottom_right[0][0]] # Slicing to crop the image
    cv2.imwrite("Cropped.jpg", cropped_source);


source = cv2.imread("pizza.jpg",1)
# Make a dummy image, will be useful to clear the drawing
dummy = source.copy()
cv2.namedWindow("Window")
# highgui function called when mouse events occur
cv2.setMouseCallback("Window", drawRectangle)
k = 0
# loop until escape character is pressed
while k!=27 :

    cv2.imshow("Window", source)
    cv2.putText(source,'''Choose top left corner, and drag - Press ESC to exit and c to clear''' ,
              (10,30), cv2.FONT_HERSHEY_SIMPLEX, 
              0.5,(255,255,255), 1 );
    k = cv2.waitKey(20) & 0xFF
    # Another way of cloning
    if k==99:
        source= dummy.copy()


cv2.destroyAllWindows()
# %%
