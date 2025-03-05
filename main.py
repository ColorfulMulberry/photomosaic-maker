import tkinter as tk
from app import App


def main():
    # create a window for the application
    root = tk.Tk(className=" Photomosaic Generator")
    root.geometry("1200x900")

    # get widgets and pack them into main window
    window = App(root)
    window.pack()

    # start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
