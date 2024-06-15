import cv2
import numpy as np

# This function requires a filename of the image and imgSize.
# imgSize is a number the final cropped square image must be dividable by, in both the width and the height.


def mouse_crop(event, x_crop, y_crop, flags, param):
    global x_start_crop, y_start_crop, x_end_crop, y_end_crop, cropping, initialCrop
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start_crop, y_start_crop, x_end_crop, y_end_crop = x_crop, y_crop, x_crop, y_crop
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            sideLength = max(abs(x_crop-x_start_crop), abs(y_crop-y_start_crop))
            try:
                x_end_crop, y_end_crop = int(x_start_crop+((x_crop-x_start_crop)/abs(x_crop-x_start_crop)*sideLength)), int(y_start_crop+((y_crop-y_start_crop)/abs(y_crop-y_start_crop)*sideLength))
            except:
                x_end_crop, y_end_crop = x_start_crop, y_start_crop
    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        initialCrop = True

def mouse_crop_adjust(event, x_crop, y_crop, flags, param):
    global x_start_crop, y_start_crop, x_end_crop, y_end_crop, cropping, moveStartCrop, moveEndCrop, moveCrop, previous_x_crop, previous_y_crop, croppedimg
    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        if abs(x_crop-x_start_crop) < 10 and abs(y_crop-y_start_crop) < 10:
            moveStartCrop = True
            moveEndCrop = False
            moveCrop = False
        elif abs(x_crop-x_end_crop) < 5 and abs(y_crop-y_end_crop) < 5:
            moveStartCrop = False
            moveEndCrop = True
            moveCrop = False
        elif x_start_crop < x_crop < x_end_crop and y_start_crop < y_crop < y_end_crop:
            moveStartCrop = False
            moveEndCrop = False
            moveCrop = True
        else:
            moveStartCrop = False
            moveEndCrop = False
            moveCrop = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            if moveStartCrop:
                sideLength = max(abs(x_crop-x_end_crop), abs(y_crop-y_end_crop))
                try:
                    x_start_crop, y_start_crop = int(x_end_crop+((x_crop-x_end_crop)/abs(x_crop-x_end_crop)*sideLength)), int(y_end_crop+((y_crop-y_end_crop)/abs(y_crop-y_end_crop)*sideLength))
                except:
                    pass
            elif moveEndCrop:
                sideLength = max(abs(x_crop-x_start_crop), abs(y_crop-y_start_crop))
                try:
                    x_end_crop, y_end_crop = int(x_start_crop+((x_crop-x_start_crop)/abs(x_crop-x_start_crop)*sideLength)), int(y_start_crop+((y_crop-y_start_crop)/abs(y_crop-y_start_crop)*sideLength))
                except:
                    pass
            elif moveCrop:
                x_start_crop = x_start_crop+x_crop-previous_x_crop
                y_start_crop = y_start_crop+y_crop-previous_y_crop
                x_end_crop = x_end_crop+x_crop-previous_x_crop
                y_end_crop = y_end_crop+y_crop-previous_y_crop
    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        if x_end_crop < x_start_crop:
            x_start_crop = x_start_crop+x_end_crop
            x_end_crop = x_start_crop-x_end_crop
            x_start_crop = x_start_crop-x_end_crop
        if y_end_crop < y_start_crop:
            y_start_crop = y_start_crop+y_end_crop
            y_end_crop = y_start_crop-y_end_crop
            y_start_crop = y_start_crop-y_end_crop
        refPoint = [(x_start_crop, y_start_crop), (x_end_crop, y_end_crop)]
        if len(refPoint) == 2: #when two points were found
            croppedimg = image[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
    previous_x_crop = x_crop
    previous_y_crop = y_crop

def ImgCropper (filename, imgSize):
    global image, cropping, initialCrop, x_start_crop, x_end_crop, y_start_crop, y_end_crop, croppedimg
    cropping = False
    initialCrop = False
    x_start_crop, y_start_crop, x_end_crop, y_end_crop = 0, 0, 0, 0
    cv2.namedWindow("image")
    cv2.setWindowProperty("image", cv2.WND_PROP_TOPMOST, 1)
    cv2.moveWindow("image", 20,20)
    image = cv2.imread(filename)
    height,width,_ = image.shape
    print('Select the desired region of the image and press "C" to confirm.')
    if max(width,height) < 850:
        if width > height:
            image = cv2.resize(image, (850,int(height*(850/width))), interpolation=cv2.INTER_NEAREST)
        else:
            image = cv2.resize(image, (int(width*(850/height)), 850), interpolation=cv2.INTER_NEAREST)
    else:
        if width > height:
            image = cv2.resize(image, (850,int(height*(850/width))))
        else:
            image = cv2.resize(image, (int(width*(850/height)), 850))
    cv2.setMouseCallback("image", mouse_crop)

    while True:
        imagegui = image.copy()
        if not cropping:
            cv2.imshow("image", image)
        elif cropping:
            cv2.rectangle(imagegui, (x_start_crop, y_start_crop), (x_end_crop, y_end_crop), (255, 0, 0), 2)
            cv2.imshow("image", imagegui)
        if initialCrop:
            break
        if cv2.waitKey(1) == 27:
            exit()

    if x_end_crop < x_start_crop:
        x_start_crop = x_start_crop+x_end_crop
        x_end_crop = x_start_crop-x_end_crop
        x_start_crop = x_start_crop-x_end_crop
    if y_end_crop < y_start_crop:
        y_start_crop = y_start_crop+y_end_crop
        y_end_crop = y_start_crop-y_end_crop
        y_start_crop = y_start_crop-y_end_crop
    refPoint = [(x_start_crop, y_start_crop), (x_end_crop, y_end_crop)]
    if len(refPoint) == 2: #when two points were found
        croppedimg = image[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]

    cv2.namedWindow("Cropped image")
    cv2.setWindowProperty("Cropped image", cv2.WND_PROP_TOPMOST, 1)
    cv2.moveWindow("Cropped image", 960,20)
    cv2.setMouseCallback("image", mouse_crop_adjust)
    while True:
        imagegui = image.copy()
        cv2.rectangle(imagegui, (x_start_crop, y_start_crop), (x_end_crop, y_end_crop), (255, 0, 0), 2)
        cv2.circle(imagegui, (x_start_crop,y_start_crop), 5, (0,255,0), -1)
        cv2.circle(imagegui, (x_end_crop,y_end_crop), 5, (0,255,0), -1)
        cv2.imshow("image", imagegui)
        try:
            cv2.imshow("Cropped image", croppedimg)
        except:
            pass
        key = cv2.waitKey(1)
        if key == 27:
            exit()
        if key == ord('c'):
            break
    cv2.destroyAllWindows()
    height, width, _ = croppedimg.shape
    if height >=imgSize:
        croppedimg = cv2.resize(croppedimg, (width-(width%imgSize), height-(height%imgSize)), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite("result.png", croppedimg)
    else:
        cv2.imwrite("result.png", np.zeros((imgSize, imgSize, 3), dtype=np.uint8))