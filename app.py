from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd
import imagehash


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # create a title label
        self.w = tk.Label(
            self,
            text="Photomosaic Generator",
            bg="#A0C0BC",
            font=("Verdana", 25, "italic"),
            padx=20,
            pady=20,
            bd=5,
            relief=tk.RIDGE,
        )
        # add widget to the window
        self.w.pack(pady=100)

        # create input image selection button
        self.input_image_btn = tk.Button(
            self,
            text="Choose the Original Image (Input)",
            font=("Verdana", 15),
            bg="#74b0cb",
            activeforeground="white",
            activebackground="#3280a2",
            cursor="hand2",
            command=self.set_input_img,
        )
        self.input_image_btn.pack()

        # create button to select multiple source images, which recreate the input
        self.src_img_btn = tk.Button(
            self,
            text="Select Smaller Images (Sources)",
            font=("Verdana", 15),
            bg="#74b0cb",
            activeforeground="white",
            activebackground="#3280a2",
            cursor="hand2",
            command=self.open_src_imgs,
        )
        self.src_img_btn.pack(pady=30)

        # create button to generate the photomosaic
        self.make_pm_btn = tk.Button(
            self,
            text="Create Photomosaic",
            font=("Verdana", 15),
            bg="#74b0cb",
            activeforeground="white",
            activebackground="#3280a2",
            cursor="hand2",
            command=self.make_photomosaic,
        )
        self.make_pm_btn.pack()

        # create a status label to display status and error messages
        self.status_label = tk.Label(
            self,
            text="Please select the original image to begin.",
            bg="#f5d7d8",
            font=("Verdana", 15, "bold"),
            padx=20,
            pady=20,
            bd=4,
            relief=tk.RIDGE,
            wraplength=750,
        )
        self.status_label.pack(pady=70)

    # extract the filename without the names of parent directories from a file pointer string
    def trim_filename(self, str):
        return str.split("/")[-1]

    # opens the file explorer to choose the input (original) image of the photomosaic
    def set_input_img(self):
        img_path = fd.askopenfilename(
            initialdir="/",
            title="Select an Image File",
            filetypes=[("Image Filetypes", "*.png *.jpg *.jpeg")],
        )
        try:
            self.input_img = Image.open(img_path)
        except FileNotFoundError:  # incorrect file pointer
            self.status_label.config(text="Input image file could not be found.")
            print("Image file could not be found")
        except AttributeError:  # no file pointer set
            self.status_label.config(text="Input image not set. Choose an image first.")
            print("Input image not set. Choose an image first.")
        else:
            self.status_label.config(
                text=self.trim_filename(img_path)
                + " selected as the input image. Its dimensions are "
                + str(self.input_img.width)
                + "x"
                + str(self.input_img.height)
                + "."
            )

    # opens the file explorer to choose the source (smaller) images for the photomosaic
    def open_src_imgs(self):
        self.src_img_list = fd.askopenfilenames(
            initialdir="/",
            title="Select multiple images",
            filetypes=[("Image Filetypes", "*.png *.jpg *.jpeg")],
        )

        src_str_list = ""  # store image names for status display
        self.src_hashes = {}  # store hashes for efficient comparison
        self.src_imgs = {}  # store images for pasting onto original image
        for src_img in self.src_img_list:
            try:
                self.src_imgs[src_img] = Image.open(src_img)
            except FileNotFoundError:  # incorrect file pointer
                self.status_label.config(text="Source image file could not be found.")
                print("Source image file could not be found.")
            else:
                if src_str_list != "":
                    src_str_list = src_str_list + ", " + self.trim_filename(src_img)
                else:
                    src_str_list = src_str_list + self.trim_filename(src_img)
        if self.src_imgs:  # if hash list non-empty display list
            self.status_label.config(text=src_str_list + " selected as source images.")
        else:
            self.status_label.config(text="No source images selected.")
            print("No source images selected.")

    # resize source images to match the box size
    def resize_hash_src_imgs(self):
        # resize each source image to the selected box size
        for filepath, im in self.src_imgs.items():
            self.src_imgs[filepath] = im.resize(
                (self.box_size, self.box_size)
            )  # change this to be scale value
            self.src_hashes[filepath] = imagehash.colorhash(
                self.src_imgs[filepath], binbits=3
            )
            print(self.src_hashes[filepath])

    # resize input image size to be divisible by the box size
    def resize_input_img(self):
        # resize input image to be divisible by the box size
        self.input_og_width, self.input_og_height = self.input_img.size

        # resize input img if width not divisible by square size
        if self.input_og_width % self.box_size == 0:
            self.input_new_width = self.input_og_width
        else:
            self.input_new_width = self.input_og_width + (
                self.box_size - (self.input_og_width % self.box_size)
            )
        # resize input img if height not divisible by square size
        if self.input_og_height % self.box_size == 0:
            self.input_new_height = self.input_og_height
        else:
            self.input_new_height = self.input_og_height + (
                self.box_size - (self.input_og_height % self.box_size)
            )
        self.input_img = self.input_img.resize(
            (self.input_new_width, self.input_new_height)
        )
        print(
            "new input img width: ",
            self.input_new_width,
            "new input img height: ",
            self.input_new_height,
        )

    # check that the images have been set before creating mosaic
    def check_creation_reqs(self):
        # input image attribute does not exist or is empty
        if not hasattr(self, "input_img") or not self.input_img:
            self.status_label.config(
                text="Input image must be selected before creating the photomosaic."
            )
            return False
        # source image attribute does not exist or is empty
        elif not hasattr(self, "src_imgs") or not self.src_imgs:
            self.status_label.config(
                text="Source images must be selected before creating the photomosaic."
            )
            return False
        else:
            return True

    # create the photomosaic using input image and source images
    def make_photomosaic(self):
        self.box_size = 20

        # check that source and input images are set
        if not self.check_creation_reqs():
            return

        # perform necessary resizing on source and input images
        self.resize_hash_src_imgs()
        self.resize_input_img()

        # number of iterations lengthwise and heightwise
        x_times, y_times = (
            self.input_new_width // self.box_size,
            self.input_new_height // self.box_size,
        )

        self.status_label.config(text="Generating the photomosaic...")
        print("Generating photomosaic...")
        hash_dict = {}  # holds results from previous hamming dist calculations to optimize
        for y in range(y_times):
            print("Replacing line ", y + 1)
            for x in range(x_times):
                # this box represents an individual square on the input image
                box = (
                    x * self.box_size,
                    y * self.box_size,
                    x * self.box_size + self.box_size,
                    y * self.box_size + self.box_size,
                )
                region = self.input_img.crop(box)
                input_hash = imagehash.colorhash(region, binbits=3)
                if input_hash in hash_dict:  # if calc previously done, use stored value
                    self.input_img.paste(self.src_imgs[hash_dict[input_hash]], box)
                else:
                    cur_best_im = None
                    cur_best_score = None
                    # calculate hamming distance for each image against the cropped square
                    for filepath, im_hash in self.src_hashes.items():
                        if cur_best_score is not None:
                            res = input_hash - im_hash
                            if res < cur_best_score:
                                cur_best_score = res
                                cur_best_im = filepath
                        else:  # if this is the first calculation, store it regardless of score
                            cur_best_score = input_hash - im_hash
                            cur_best_im = filepath
                    self.input_img.paste(self.src_imgs[cur_best_im], box)
        # save the image, rescale back to original size OR rescale to given size
        self.input_img.save("edited.png")
        self.status_label.config(text="Photomosaic saved as edited.png")
        print("Photomosaic saved as edited.png")
