from PIL import Image
import tkinter as tk
from tkinter import filedialog as fd
import imagehash


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # create a title label
        self.title = tk.Label(
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
        self.title.pack(pady=40)

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

        # create slider to choose size of squares
        self.size_scale = tk.Scale(
            self,
            from_=5,
            to=100,
            orient=tk.HORIZONTAL,
            label="    Square Size:",
            font=("Verdana", 15),
            length=200,
        )
        self.size_scale.pack()
        self.size_scale.set(20)  # set the initial box size value

        # create slider to choose how much to enlarge the output image compared to input
        self.enlarge_scale = tk.Scale(
            self,
            from_=1,
            to=15,
            orient=tk.HORIZONTAL,
            label=" Enlarge Output:",
            font=("Verdana", 15),
            length=200,
        )
        self.enlarge_scale.pack()
        self.enlarge_scale.set(1)  # set the initial multiplier value

        # create button to generate the photomosaic
        self.photomosaic_btn = tk.Button(
            self,
            text="Create Photomosaic",
            font=("Verdana", 15),
            bg="#74b0cb",
            activeforeground="white",
            activebackground="#3280a2",
            cursor="hand2",
            command=self.make_photomosaic,
        )
        self.photomosaic_btn.pack(pady=20)

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
        self.status_label.pack(pady=50)

        # create an input status label to show selected input image
        self.input_status = tk.Label(
            self,
            text="Input image: None selected.",
            bg="#c4c5c6",
            font=("Verdana", 14, "italic"),
            pady=13,
            bd=4,
            relief=tk.RIDGE,
            width=50,
        )
        self.input_status.pack()

        # create an input status label to show selected input image
        self.source_status = tk.Label(
            self,
            text="Source images: None selected.",
            bg="#c4c5c6",
            font=("Verdana", 14, "italic"),
            pady=13,
            bd=4,
            relief=tk.RIDGE,
            width=50,
        )
        self.source_status.pack()

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
        # file path not empty
        if img_path:
            try:
                self.input_img = Image.open(img_path)
            except FileNotFoundError:  # incorrect file pointer
                self.status_label.config(text="Input image file could not be found.")
                print("Image file could not be found")
            except AttributeError:  # no file pointer set
                self.status_label.config(
                    text="Input image not set. Choose an image first."
                )
                print("Input image not set. Choose an image first.")
            else:
                flname = self.trim_filename(img_path)
                self.status_label.config(
                    text=flname
                    + " selected as the input image. Its dimensions are "
                    + str(self.input_img.width)
                    + "x"
                    + str(self.input_img.height)
                    + "."
                )
                if len(flname) > 15:  # trim name if too long
                    flname = flname[:15] + "..."
                self.input_status.config(
                    text="Input image: "
                    + flname
                    + "   Size: "
                    + str(self.input_img.width)
                    + "x"
                    + str(self.input_img.height)
                )
        else:
            self.input_status.config(text="Input image: None selected.")

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
                print("Source image file could not be found.")
            else:
                if src_str_list != "":
                    src_str_list = src_str_list + ", " + self.trim_filename(src_img)
                else:
                    src_str_list = src_str_list + self.trim_filename(src_img)
        if self.src_imgs:  # if hash list non-empty display list
            if len(src_str_list) > 50:
                self.status_label.config(
                    text=src_str_list[:50] + "... selected as source images."
                )
            else:
                self.status_label.config(
                    text=src_str_list + " selected as source images."
                )
            self.source_status.config(
                text="Source images: " + str(len(self.src_img_list)) + " selected."
            )
        else:
            self.status_label.config(text="No source images selected.")
            self.source_status.config(text="Source images: None selected.")

    # resize source images to match the box size
    def resize_hash_src_imgs(self):
        # resize each source image to the selected box size
        for filepath, im in self.src_imgs.items():
            self.src_imgs[filepath] = im.resize(
                (self.box_size, self.box_size)
            )  # change this to be scale value
            self.src_hashes[filepath] = imagehash.colorhash(
                self.src_imgs[filepath], binbits=6
            )
            print(self.src_hashes[filepath])

    # resize input image size to be divisible by the box size
    def resize_input_img(self):
        # resize input image to be divisible by the box size
        self.input_og_width, self.input_og_height = (
            self.input_img.width * self.resize_amt,
            self.input_img.height * self.resize_amt,
        )

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
        self.output_img = self.input_img.resize(
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
        # check that source and input images are set
        if not self.check_creation_reqs():
            return

        self.box_size = self.size_scale.get()
        self.resize_amt = self.enlarge_scale.get()

        # perform necessary resizing on source and input images
        self.resize_hash_src_imgs()
        self.resize_input_img()

        print("Generating photomosaic...")
        hash_dict = {}  # holds results from previous hamming dist calculations to optimize

        # number of iterations lengthwise and heightwise
        x_times, y_times = (
            self.input_new_width // self.box_size,
            self.input_new_height // self.box_size,
        )

        for y in range(y_times):
            print("Replacing row", y + 1)
            for x in range(x_times):
                # this box represents an individual square on the input image
                box = (
                    x * self.box_size,
                    y * self.box_size,
                    x * self.box_size + self.box_size,
                    y * self.box_size + self.box_size,
                )
                region = self.output_img.crop(box)
                input_hash = imagehash.colorhash(region, binbits=6)

                if input_hash in hash_dict:  # if calc previously done, use stored value
                    self.output_img.paste(self.src_imgs[hash_dict[input_hash]], box)
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
                    self.output_img.paste(self.src_imgs[cur_best_im], box)

        # save the image, rescale back to original size OR rescale to given size
        # maybe make this part into a function
        self.output_img.save("edited.png")
        self.status_label.config(text="Photomosaic saved as edited.png")
        print("Photomosaic saved as edited.png")
