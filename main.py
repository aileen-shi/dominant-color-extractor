from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
import pathlib
import cv2
from sklearn.cluster import KMeans
import numpy as np

valid = False
file_path = None


class PaletteColors:
    """This is a class for generating colors from an image.

    Attributes:
        colors (float): Array of clusters containing rgb values.
        image (str): The name of the image file.
    """
    colors = None

    def __init__(self, image):
        """The constructor for PaletteColors.

        Args:
            image (str): The name of the image file.
        """
        self.image = image

    def calc_colors(self):
        """Classify the 4 main image colors.

        Returns:
            int: Array of rgb values
        """
        img_cv2 = cv2.imread(self.image)
        img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        img_cv2 = img_cv2.reshape((img_cv2.shape[0] * img_cv2.shape[1]), 3)

        kmeans = KMeans(n_clusters=4, random_state=0, n_init='auto')
        kmeans.fit(img_cv2)

        self.colors = kmeans.cluster_centers_

        return self.colors.astype(int)


def check_file(file):
    """Check if a file is an image.

    Args:
        file (str): Name of the file.

    Returns:
        bool: True if png or jpg, False otherwise.
    """
    file_ext = pathlib.Path(file).suffix

    if file_ext != ".png" and file_ext != ".jpg" and file_ext:
        messagebox.showwarning("Warning", "Select a png or jpg")
        return False

    global valid
    valid = True

    return True


def get_ratio(pic):
    """Calculate aspect ratio.

    Args:
        pic (Image): The image.

    Returns:
        float: The aspect ratio.
    """
    MAX_WIDTH = 500
    MAX_HEIGHT = 300
    width = pic.width
    height = pic.height
    ratio = min(MAX_WIDTH / width, MAX_HEIGHT / height)
    return ratio


def update_buttons():
    """Update button colors."""
    generate.configure(background=color4)
    export.configure(background=color4)


def open_file():
    """Open file command for upload button"""
    global file_path
    file_path = filedialog.askopenfilename()

    if check_file(file_path):
        pic = Image.open(file_path)
        ratio = get_ratio(pic)
        resize = pic.resize((int(pic.width * ratio), int(pic.height * ratio)))
        converted_img = ImageTk.PhotoImage(resize)
        img.configure(image=converted_img, bg=color3)
        img.image = converted_img
        update_buttons()


def rgb_hex(rgb):
    """Convert rgb values to hex.

    Args:
        rgb(int): Array of rgb values

    Returns:
        str: Array of hex values
    """
    hex_val = np.empty((1, 4), dtype=object)
    for i in range(4):
        r = rgb[i][0]
        g = rgb[i][1]
        b = rgb[i][2]
        hex_val[0][i] = ('#{:02x}{:02x}{:02x}'.format(r, g, b))
    return hex_val


def show_colors(colors):
    """Display color palette

    Args:
        colors (str): Array of hex color values
    """
    cell1.configure(bg=colors[0][0])
    cell2.configure(bg=colors[0][1])
    cell3.configure(bg=colors[0][2])
    cell4.configure(bg=colors[0][3])


def generate_button():
    """Command for generate button to generate colors."""
    global valid
    if valid:
        global file_path
        palette_colors = PaletteColors(file_path)
        colors = palette_colors.calc_colors()
        rgb_colors = rgb_hex(colors)
        show_colors(rgb_colors)
    else:
        messagebox.showerror("Error", "Please upload an image first")


def screenshot():
    """Command for export button to capture screen"""
    global valid
    if valid:
        pic = ImageGrab.grab(bbox=None)
        pic.show()
    else:
        messagebox.showerror("Error", "Please upload an image first")


# Color Scheme
color1 = '#282a2b'
color2 = '#313436'
color3 = '#393b3d'
color4 = '#1871a8'
color5 = '#4daae3'
color6 = '#5b5f63'

# Window
root = Tk()
root.geometry('900x600')
root.resizable(width=False, height=False)
root.title("Color Palette Generator")
icon = PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.config(background=color6)

# Left Frame
left_frame = Frame(root, bg=color1, width=300, height=600)
left_frame.grid(row=0, column=0)
left_frame.grid_propagate(False)

# Toolbar
tool_bar = Frame(left_frame, bg=color1, width=260, height=300)
tool_bar.grid(row=0, column=0, padx=20, pady=150)

# Upload Button
upload = Button(
    tool_bar,
    background=color4,
    foreground=color1,
    activebackground=color5,
    border=0,
    height=2,
    width=20,
    text='Upload',
    font=('Arial', 16, 'bold'),
    command=open_file
)
upload.grid(column=0, row=0, pady=10)

# Generate Button
generate = Button(
    tool_bar,
    background=color6,
    foreground=color1,
    activebackground=color5,
    border=0,
    height=2,
    width=20,
    text='Generate',
    font=('Arial', 16, 'bold'),
    command=generate_button
)
generate.grid(column=0, row=1, pady=20)

# Export Button
export = Button(
    tool_bar,
    background=color6,
    foreground=color1,
    activebackground=color5,
    border=0,
    height=2,
    width=20,
    text='Export',
    font=('Arial', 16, 'bold'),
    command=screenshot
)
export.grid(column=0, row=2, pady=10)

# Right Frame
right_frame = Frame(root, bg=color3, width=600, height=600)
right_frame.grid(row=0, column=1)

# Image Frame
image_frame = Frame(right_frame, bg=color3, width=500, height=300)
image_frame.grid(row=0, column=0, pady=50)
image_frame.grid_propagate(False)

# Image
img = Label(image_frame, width=500, height=300, bg=color6)
img.grid(row=0, column=0)

# Swatches Frame
swatches = Frame(right_frame, bg=color2, width=600, height=200)
swatches.grid(row=1, column=0)

# Swatch Bar Frame
swatch_bar = Frame(swatches, bg=color2, width=560, height=160)
swatch_bar.grid(row=0, column=0, padx=20, pady=20)

# Color Palette Cells
cell1 = Frame(swatch_bar, bg=color6, width=120, height=120)
cell1.grid(row=0, column=0, padx=10, pady=20)
cell2 = Frame(swatch_bar, bg=color6, width=120, height=120)
cell2.grid(row=0, column=1, padx=10, pady=20)
cell3 = Frame(swatch_bar, bg=color6, width=120, height=120)
cell3.grid(row=0, column=2, padx=10, pady=20)
cell4 = Frame(swatch_bar, bg=color6, width=120, height=120)
cell4.grid(row=0, column=3, padx=10, pady=20)

root.mainloop()
