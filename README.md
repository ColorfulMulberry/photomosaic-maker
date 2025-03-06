# photomosaic-maker
 
photomosaic-maker is a program that takes selected images from the computer and creates a photomosaic that resembles an input image.

It was implemented in Python with the [tkinter library](https://docs.python.org/3/library/tkinter.html) to create a GUI, and the [Pillow (PIL fork) library](https://pillow.readthedocs.io/en/stable/) for image processing/comparisons.

![edited](https://github.com/user-attachments/assets/30e63fcd-1846-4f56-8710-111bb5392e74)

## Installation (Windows)

* Download the latest release from the [releases folder](https://github.com/ColorfulMulberry/photomosaic-maker/releases).

* Alternatively, download the source code and run it yourself if you prefer.

*Note: It is possible that Windows or your anti-virus will flag the file as potentially dangerous, since it is a simple executable file. Run it through [Virustotal](https://www.virustotal.com/gui/home/upload) or scan it with your anti-virus and decide for yourself whether or not to use it.*

## How to use

1. Download the latest release file.
   
2. Run `main.exe`. A graphical window and a terminal will pop-up.

3. Select an input image using the `Choose the Original Image (Input)` button. This is the image that will be converted into a photomosaic at the end of the process.

4. Choose multiple source images with the `Select Smaller Images (Sources)` button. which will be pasted onto the output image, recreating the input image. Choose at least 50 or more images for a good result, with a wide variety of color palettes.
   
   Sample images can be [found here](https://github.com/ColorfulMulberry/photomosaic-maker/raw/refs/heads/main/sample_imgs/sample_imgs.zip), sourced from Pixabay. Download and unzip `sample_imgs.zip` in order to use them.

5. Adjust the size of the individual squares as needed using the `Square Size` slider. This will affect the size of each source image on the output image.

6. Modify the output image's size as needed using the `Enlarge Output` slider. The multiplier is relative to the input image's size.

7. After confirming that input and source images have been selected, create a photomosaic by pressing the `Create Photomosaic` button.

8. The photomosaic creation process can take some time, so watch the terminal to ensure that it is still running.

9. After the output image has been created, it will be saved to the same folder that the program is stored in. Navigate to it to see the results.

## Tips/Advice

* To add more detail to the output image, either decrease `Square Size`, or increase `Enlarge Output`.

* Increase `Square Size` to see more detail in the source images.

* Choose a variety of images (50 or more recommended) with a large range of colors. Choosing few/similar images will likely result in a lackluster output image.

## Additional Examples

Examples below use the [sample_imgs](https://github.com/ColorfulMulberry/photomosaic-maker/raw/refs/heads/main/sample_imgs/sample_imgs.zip) folder as source images. Download and unzip `sample_imgs.zip` in order to use them.

### Original
![pie-5601656_1920](https://github.com/user-attachments/assets/23c0b8e5-9ebf-4bc1-bcba-3642dd3f698e)

### Square Size: 25, Enlarge Output: 1.5
![edited](https://github.com/user-attachments/assets/d5d5eca1-e96b-4265-80e0-14f977225a3c)

### Original
![roller-coaster-7942853_1920](https://github.com/user-attachments/assets/3d36ae2a-bb79-4069-acd5-c301d5254bc9)

### Square Size: 25, Enlarge Output: 2.0
![edited](https://github.com/user-attachments/assets/b3f8b38f-cbcf-4d96-8ba7-77504170ad61)

### Original
![gruner-tee-7807229_1920](https://github.com/user-attachments/assets/4fd0dbc1-89c8-44bf-88ae-6647235c7788)

### Square Size: 20, Enlarge Output: 1.0
![edited](https://github.com/user-attachments/assets/86b2ec87-681a-43bb-8406-87bded45fcea)
