# AI-LEGO-PixelArt-Robot

This is the code for my AI Lego pixelart robot, as seen on my YouTube channel:
<div align="left">
  <a href="https://www.youtube.com/watch?v=ec_BtS97IR8"><img src="https://img.youtube.com/vi/ec_BtS97IR8/0.jpg" alt="IMAGE ALT TEXT"></a>
</div>

The code generates pixelart using OpenAI's Dall-E 3 and controls a Lego Pixelart machine using Mindstorms.
It was meant for personal use, so it will not work right away and it will need many changes.
I am not updating this project, so libraries like openai might get outdated.
This code was last succesfully tested on 6/15/2024.


## For use of "main.py"

### Some things to note
- You will need to get your own OpenAI API key and rename the variable in the "imageGenerator.py" file.
- You will need to change the Bluetooth address of your Mindstorms in the "main.py" file.
- You can define the usable colors by changing the list "colors_bgr" and "colors_stock" in "main.py" and "recipe" in "imageFunctions.py". They are in the correct order from furthest away from the bed to closest by the bed.
- You will need to set all the variables that specify motor positions in "main.py" to work with your machine.
- You will need to define all the motors and sensors correctly in "main.py", with correct ports, speeds and directions.
- You might need to adjust motor speeds in "ev3Functions.py".

### Some things that can be changed
- You can switch whether you want to use a custom image or use the image generator with the variable "useAI" in "main.py".
- You can define your object or filepath by renaming the variables in "main.py".
- You can change the pixelart size by changing the "imgSize" variable in "main.py".
- "usepixelation" in "main.py" changes the code to either scale images down to the desired size or pick the center point of a grid to create a crisp pixelart.
- "useOverlay" in "main.py" switches on or off the Lego overlay on the final image.
- You can define how many usable pixels are in the hoppers, before it prompts you to refill the hoppers, by changing the "color_amount" variable in "main.py".


## For use of "main (NO Mindstorms).py"

### Some things to note
- You will need to get your own OpenAI API key and rename the variable in the "imageGenerator.py" file.
- You can define the usable colors by changing the list "colors_bgr" and "colors_stock" in "main (NO Mindstorms).py" and "recipe" in "imageFunctions.py".

### Some things that can be changed
- You can switch whether you want to use a custom image or use the image generator with the variable "useAI" in "main (NO Mindstorms).py".
- You can define your object or filepath by renaming the variables in "main (NO Mindstorms).py".
- You can change the pixelart size by changing the "imgSize" variable in "main (NO Mindstorms).py".
- "usepixelation" in "main (NO Mindstorms).py" changes the code to either scale images down to the desired size or pick the center point of a grid to create a crisp pixelart.
- "useOverlay" in "main (NO Mindstorms).py" switches on or off the Lego overlay on the final image.
- You can define how many usable pixels are in the hoppers, before it prompts you to refill the hoppers, by changing the "color_amount" variable in "main (NO Mindstorms).py".
