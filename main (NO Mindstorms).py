import cv2
import imageFunctions
import imageGenerator
import imageCropper
import numpy as np
import blend_modes

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
print('Starting...\nPress "A" to Abort code early.\n')
coords = list((int(0),int(0)))
while True:

    # Get current pixel color
    current_color = list(simplified_image[imgSize-coords[1]-1, coords[0]])
    
    # Get current color index
    current_color_index = list(colors_bgr.values()).index((current_color[0], current_color[1], current_color[2]))

    # Check if current pixel color isn't white
    if current_color != list((255,255,255)):

        # Checking whether the desired color is present
        current_color_name = list(colors_bgr.keys())[list(colors_bgr.values()).index((current_color[0], current_color[1], current_color[2]))]
        if colors_stock[current_color_name] > 0:
            colors_stock[current_color_name] -= 1

        # Ask for refill if needed
        else:
            print("Please refill all colors, because", current_color_name, 'is almost empty.\nPress "F" to finish fill.')
            while True:
                if cv2.waitKey(1) == ord('f'): break
            for x in colors_stock:
                colors_stock[x] = color_amount
            print("Resetting Z-Axis...")
            print("Resetting X-Axis...")

        # Update current image
        current_image[imgSize-coords[1]-1, coords[0]] = current_color
        if useOverlay: cv2.imshow("Current Image", blend_modes.multiply(np.dstack((cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST), np.ones((512, 512, 1), dtype=float))), legoOverlay, 1).astype(np.uint8))
        else: cv2.imshow("Current Image", cv2.resize(current_image, (512, 512), interpolation=cv2.INTER_NEAREST))

    # Going to the next pixel
    if coords[0] < 31: coords[0] += 1
    else: coords[0] = 0; coords[1] += 1

    # Checking whether the code should be ended
    if cv2.waitKey(1) == ord('a'): break
    if coords[1] == 32: break
cv2.destroyAllWindows()