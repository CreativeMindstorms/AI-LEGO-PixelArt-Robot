import cv2
import imageFunctions
import imageGenerator
import imageCropper
import ev3_dc
from time import sleep
import numpy as np
import blend_modes
import ev3Functions

# whether to use AI or a custom image
useAI = False

# Prompt describing the desired image
object = "desired image"

# Filename of the custom image
filename = "customImage.png"

# Variables for the pixelation algorithm
usepixelation = True
imgSize = 32

# whether to use the lego overlay on images
useOverlay = True
legoOverlay = cv2.imread("lego_overlay.png", -1).astype(float)

# Motor positions in degrees
Xstart    = -680    # Above dark bluish gray (from touching the sensor)
Xend      = -5860   # Above black (from Xstart)
Xright    = -6535   # Above right row (from Xstart)
Xleft     = -134850  # Above left row (from Xstart)
Xdistance =  50     # Distance to the right of the desired location to start moving slowly

Ystart    =  110    # Above bottom row (from touching the sensor)
Yend      = -13990  # Above top row (from Ystart)
Yfinish   = -15360  # Fully towards user on display (from Ystart)
Ydistance =  100     # Distance to the desired location to start moving slowly

Zbottom   = -330    # Down (from auto starting position)
Ztop      =  0      # Up (from auto starting position)
Zdistance = -240    # Hovering above down (from auto starting position)

# Define the BGR values of Lego colors
colors_bgr = {
    'white': (255,255,255),
    'dark bluish gray': (104, 110, 108),
    'light bluish gray': (169, 165, 160),
    'tan': (158,205,228),
    'reddish brown': (18,42,88),
    'bright pink': (200,173,228),
    'dark purple': (145,54,63),
    'blue': (191,85,0),
    'dark azure': (201,139,7),
    'green': (65,120,35),
    'lime': (11,233,187),
    'yellow': (55,205,242),
    'orange': (24,138,254),
    'red': (9,26,201),
    'black': (0,0,0)
}

# Define the amount of usable Lego bricks in the machine
color_amount = 23
colors_stock = {
    'dark bluish gray': color_amount,
    'light bluish gray': color_amount,
    'tan': color_amount,
    'reddish brown': color_amount,
    'bright pink': color_amount,
    'dark purple': color_amount,
    'blue': color_amount,
    'dark azure': color_amount,
    'green': color_amount,
    'lime': color_amount,
    'yellow': color_amount,
    'orange': color_amount,
    'red': color_amount,
    'black': color_amount
}


# Connect to the Mindstorms brick
ev3 = ev3_dc.EV3(protocol=ev3_dc.BLUETOOTH, host='YOUR MINDSTORMS')       # EV3
print(ev3)

# Define motors and sensors
Xmotor = ev3_dc.Motor(ev3_dc.PORT_A, ev3_obj=ev3)
Ymotor = ev3_dc.Motor(ev3_dc.PORT_B, ev3_obj=ev3)
Zmotor = ev3_dc.Motor(ev3_dc.PORT_C, ev3_obj=ev3)
XTouch = ev3_dc.Touch(ev3_dc.PORT_1, ev3_obj=ev3)
YTouch = ev3_dc.Touch(ev3_dc.PORT_2, ev3_obj=ev3)

# Setting motorproperties
Xmotor.speed = 10
Ymotor.speed = 10
Zmotor.speed = 50
Xmotor.directoin = 1  # positive: right
Ymotor.direction = -1 # positive: top (of image)
Zmotor.direction = 1  # positive: up


# Create an image for the machine. Saved as "result.jpg"
if useAI:
    AIfilename = "AIresult.png"
    print(f'\nGenerating image from prompt: "{object}"\n')
    imageGenerator.AIGenerator(object, AIfilename)
    imageFunctions.confirm_image(imgSize, object, AIfilename)
else:
    print(f'\nGetting image from path: "{filename}"\n')
    imageCropper.ImgCropper(filename, imgSize)


# Read the input image
original_image = cv2.imread("result.png")

# Pixelate the image
if usepixelation:
    pixelated_image = imageFunctions.pixelate_image(original_image, imgSize)
else:
    pixelated_image = cv2.resize(original_image, (32, 32), interpolation=cv2.INTER_AREA)
cv2.imwrite("pixelart.png", cv2.resize(pixelated_image, (256, 256), interpolation=cv2.INTER_NEAREST))

# Turn it into Lego colors
simplified_image, recipe = imageFunctions.simplify_image(pixelated_image, colors_bgr)
cv2.imwrite("pixelart Lego.png", cv2.resize(simplified_image, (256, 256), interpolation=cv2.INTER_NEAREST))

# Printing the required bricks
print("Image created.\n\nRequired bricks:")
print("----------------------------")
for i in recipe: print(f"{i:<18}| {recipe[i]:>3} pcs.")
print("----------------------------")


# Display the original and pixelated images
cv2.imshow("Original Image", cv2.resize(original_image, (512, 512), interpolation=cv2.INTER_NEAREST))
cv2.setWindowProperty("Original Image", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Original Image", 136,200)
cv2.imshow("Pixelated Image", cv2.resize(pixelated_image, (512, 512), interpolation=cv2.INTER_NEAREST))
cv2.setWindowProperty("Pixelated Image", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Pixelated Image", 698,200)
if useOverlay: cv2.imshow("Final Image", blend_modes.multiply(np.dstack((cv2.resize(simplified_image, (512, 512), interpolation=cv2.INTER_NEAREST), np.ones((512, 512, 1), dtype=float))), legoOverlay, 1).astype(np.uint8))
else: cv2.imshow("Final Image", cv2.resize(simplified_image, (512, 512), interpolation=cv2.INTER_NEAREST))
cv2.setWindowProperty("Final Image", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Final Image", 1260,200)


# Asking for confirmation
print('Press "C" to Confirm.\n')
while True:
    if cv2.waitKey(1) == ord('c'): break
cv2.destroyAllWindows()


# Resetting Z-Axis
print("Resetting Z-Axis...")
ev3Functions.resetZAxis(Zmotor)

# Resetting X-Axis
print("Resetting X-Axis...")
ev3Functions.resetXAxis(Xmotor, XTouch, Xstart, Xdistance)

# Resetting Y-Axis
print("Resetting Y-Axis...\n")
ev3Functions.resetYAxis(Ymotor, YTouch, Ystart, Ydistance)


# Creating empty white image
current_image = np.full((int(imgSize), int(imgSize), 3), 255, dtype='uint8')

# Display the targeted and current image
if useOverlay: cv2.imshow("Current Image", blend_modes.multiply(np.dstack((cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST), np.ones((512, 512, 1), dtype=float))), legoOverlay, 1).astype(np.uint8))
else: cv2.imshow("Current Image", cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST))
cv2.setWindowProperty("Current Image", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Current Image", 417,200)
if useOverlay: cv2.imshow("Targeted Image", blend_modes.multiply(np.dstack((cv2.resize(simplified_image, (512, 512), interpolation=cv2.INTER_NEAREST), np.ones((512, 512, 1), dtype=float))), legoOverlay, 1).astype(np.uint8))
else: cv2.imshow("Targeted Image", cv2.resize(simplified_image, (512, 512), interpolation=cv2.INTER_NEAREST))
cv2.setWindowProperty("Targeted Image", cv2.WND_PROP_TOPMOST, 1)
cv2.moveWindow("Targeted Image", 979,200)


# Starting main loop
print('Starting...\nPress "A" to Abort code early, or "P" to pause the program.\n')
coords = list((int(0),int(0)))
while True:

    # Get current pixel color, index and name
    current_color = list(simplified_image[imgSize-coords[1]-1, coords[0]])
    current_color_index = list(colors_bgr.values()).index((current_color[0], current_color[1], current_color[2]))
    current_color_name = list(colors_bgr.keys())[list(colors_bgr.values()).index((current_color[0], current_color[1], current_color[2]))]

    # Check if current pixel color isn't white
    if current_color != list((255,255,255)):

        # Checking whether the desired color is present and subtracting one from the list
        if colors_stock[current_color_name] > 0:
            colors_stock[current_color_name] -= 1

        # Ask for refill if needed
        else:
            print("Please refill all colors, because", current_color_name, 'is almost empty.\nPress "F" to finish fill.')
            while True:
                if cv2.waitKey(1) == ord('f'): break
            for x in colors_stock:
                colors_stock[x] = color_amount
            # Resetting Z-Axis
            print("Resetting Z-Axis...")
            ev3Functions.resetZAxis(Zmotor)
            # Resetting X-Axis
            print("Resetting X-Axis...")
            ev3Functions.resetXAxis(Xmotor, XTouch, Xstart, Xdistance)

        # Move towards correct color intake
        ev3Functions.moveXmotor(Xmotor, int((current_color_index-1)*(Xend/(len(colors_bgr)-2))), Xdistance)
        
        # Checking whether the code should be aborted early or paused
        key = cv2.waitKey(1)
        if key == ord('a'): finished = False; break
        if key == ord('p'):
            while cv2.waitKey(1) != ord('c'): pass

        # Picking up the pixel
        ev3Functions.pickPixel(Zmotor, Zbottom, Ztop, Zdistance)

        # Checking whether the code should be aborted early or paused
        key = cv2.waitKey(1)
        if key == ord('a'): finished = False; break
        if key == ord('p'):
            while cv2.waitKey(1) != ord('c'): pass

        # Move towards correct X coordinate
        ev3Functions.moveXmotor(Xmotor, int(Xright+((Xleft-Xright)/(imgSize-1))*(imgSize-coords[0]-1)), Xdistance, keepDistance=True)
        
        # Checking whether the code should be aborted early or paused
        key = cv2.waitKey(1)
        if key == ord('a'): finished = False; break
        if key == ord('p'):
            while cv2.waitKey(1) != ord('c'): pass

        # Placing the pixel
        ev3Functions.placePixel(Zmotor, Xmotor, Ymotor, Zbottom, Ztop, Zdistance, int(Xright+((Xleft-Xright)/(imgSize-1))*(imgSize-coords[0]-1)), int(coords[1]*(Yend/(imgSize-1))), Ydistance)

        # Update current image
        current_image[imgSize-coords[1]-1, coords[0]] = current_color
        if useOverlay: cv2.imshow("Current Image", blend_modes.multiply(np.dstack((cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST), np.ones((512, 512, 1), dtype=float))), legoOverlay, 1).astype(np.uint8))
        else: cv2.imshow("Current Image", cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST))

    # Going to the next pixel
    if coords[0] < 31:
        coords[0] += 1
    else:
        coords[0] = 0
        coords[1] += 1

        # Moving Y-Axis if y coordinate increased
        ev3Functions.moveYmotor(Ymotor, int(coords[1]*(Yend/(imgSize-1))), Ydistance)
    

    # Checking whether the code should be ended or paused
    key = cv2.waitKey(1)
    if key == ord('a'): finished = False; break
    if coords[1] == 32: finished = True; break
    if key == ord('p'):
        while cv2.waitKey(1) != ord('c'): pass

# Close image windows
cv2.destroyAllWindows()

# Present artwork to user
if finished:
    ev3Functions.moveXmotor(Xmotor, Xstart, Xdistance)
    ev3Functions.moveYmotor(Ymotor, Yfinish, Ydistance, useYdistance=True)

# Stop sending power to the motors
sleep(1)
Xmotor.stop(brake=False)
Ymotor.stop(brake=False)
Zmotor.stop(brake=False)