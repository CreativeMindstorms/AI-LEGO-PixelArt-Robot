import numpy as np
import cv2
import imageGenerator
import imageCropper

def confirm_image(imgSize, object, AIfilename):
    original_image = cv2.imread(AIfilename)
    cv2.imwrite("result.png", original_image)
    exit_main_loop = False
    while not exit_main_loop:
        # Read and show the input image
        original_image = cv2.imread("result.png")
        cv2.imshow("Original Image", cv2.resize(original_image, (512, 512), interpolation=cv2.INTER_NEAREST))
        cv2.setWindowProperty("Original Image", cv2.WND_PROP_TOPMOST, 1)
        cv2.moveWindow("Original Image", 136,200)
        print('Image generated.\nPress: "C" to Confirm, "R" to Regenerate, "T" to Trim.')
        while True:
            key = cv2.waitKey(1)
            if key == ord('c'):
                cv2.destroyAllWindows()
                original_image = cv2.imread(AIfilename)
                cv2.imwrite("result.png", original_image)
                exit_main_loop = True
                break
            elif key == ord('r'):
                cv2.destroyAllWindows()
                print(f'\nGenerating image from prompt: "{object}"\n')
                imageGenerator.AIGenerator(object, AIfilename)
                original_image = cv2.imread(AIfilename)
                cv2.imwrite("result.png", original_image)
                break
            elif key == ord('t'):
                cv2.destroyAllWindows()
                imageCropper.ImgCropper(AIfilename, imgSize)
                exit_main_loop = True
                break

def pixelate_image(original_image, imgSize):
    height, width = original_image.shape[:2]
    rows, cols = imgSize, imgSize
    # Calculate the size of each square
    row_size = height // rows
    col_size = width // cols
    # Create a copy of the original image to apply pixelation
    pixelated_image = np.zeros((rows, cols, 3), dtype=np.uint8)

    for i in range(0, height, row_size):
        for j in range(0, width, col_size):
            center_pixel_color = original_image[i + row_size // 2, j + col_size // 2]
            pixelated_image[i//row_size, j//col_size] = center_pixel_color

    return pixelated_image

def find_closest_color(pixel, color_dict):
    pixel_array = np.array(pixel)
    color_values = np.array(list(color_dict.values()))
    distances = np.linalg.norm(color_values - pixel_array, axis=1)
    closest_color_index = np.argmin(distances)
    closest_color = list(color_dict.keys())[closest_color_index]
    
    return color_dict[closest_color], closest_color

def simplify_image(image, colors_dict):
    recipe = {
        'red': 0,
        'orange': 0,
        'yellow': 0,
        'lime': 0,
        'green': 0,
        'dark azure': 0,
        'blue': 0,
        'dark purple': 0,
        'bright pink': 0,
        'reddish brown': 0,
        'tan': 0,
        'light bluish gray': 0,
        'dark bluish gray': 0,
        'black': 0,
        'white': 0
        }
    height, width, _ = image.shape
    mapped_image = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pixel = image[i, j]
            closest_color, closest_color_name = find_closest_color(pixel, colors_dict)
            mapped_image[i, j] = closest_color
            recipe[closest_color_name] += 1
    
    del recipe['white']
    for i in list(recipe.keys()):
        if recipe[i] ==0:
            del recipe[i]

    return mapped_image, recipe