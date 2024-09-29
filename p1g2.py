import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImagePalette
import struct

class PCXViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PCX Viewer")
        self.root.geometry("800x800")

        # Add a button to open a file
        self.open_button = tk.Button(root, text="Open PCX File", command=self.open_pcx)
        self.open_button.pack(pady=20)

        # Add a label to display the image
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Add a text box to display header information
        self.header_info = tk.Text(root, height=15, width=100)
        self.header_info.pack(pady=10)

        # Add a label for the color palette
        self.palette_label = tk.Label(root)
        self.palette_label.pack()

    def open_pcx(self):
        file_path = filedialog.askopenfilename(filetypes=[("PCX files", "*.pcx")])
        if file_path:
            self.display_pcx(file_path)

    def display_pcx(self, file_path):
        with open(file_path, 'rb') as f:
            # Read the first 128 bytes of the header
            header = f.read(128)

            # Parse the header information
            manufacturer, version, encoding, bits_per_pixel = struct.unpack("4B", header[:4])
            xmin, ymin, xmax, ymax = struct.unpack("<HHHH", header[4:12])
            hdpi, vdpi = struct.unpack("<HH", header[12:16])
            num_color_planes, bytes_per_line = struct.unpack("<BxH", header[65:69])
            palette_info, h_screen_size, v_screen_size = struct.unpack("<3H", header[66:72])

            # Display header information
            info_text = f"Manufacturer: Zsoft (.pcx ({manufacturer}))\n"
            info_text += f"Version: {version}\n"
            info_text += f"Encoding: {encoding}\n"
            info_text += f"Bits per Pixel: {bits_per_pixel}\n"
            info_text += f"Image Dimensions: {xmin} {ymin} {xmax} {ymax}\n"
            info_text += f"HDPI: {hdpi}\n"
            info_text += f"VDPI: {vdpi}\n"
            info_text += f"Number of Color Planes: {num_color_planes}\n"
            info_text += f"Bytes per Line: {bytes_per_line}\n"
            info_text += f"Palette Information: {palette_info}\n"
            info_text += f"Horizontal Screen Size: {h_screen_size}\n"
            info_text += f"Vertical Screen Size: {v_screen_size}\n"
            info_text += f"Color Palette: \n"

            self.header_info.delete(1.0, tk.END)
            self.header_info.insert(tk.END, info_text)

            # Display the image using Pillow
            image = Image.open(file_path)
            image_tk = ImageTk.PhotoImage(image)
            self.image_label.config(image=image_tk)
            self.image_label.image = image_tk  # Keep a reference to avoid garbage collection

            # Move to the start of the palette (from the end of the file)
            f.seek(-769, 2)
            palette_header = f.read(1)
            if palette_header == b'\x0C':  # Confirm it's a valid palette
                palette_data = f.read(768)  # Read the palette data

                # Convert palette data to a list of (R, G, B) tuples
                colors = [tuple(palette_data[i:i+3]) for i in range(0, len(palette_data), 3)]
                
                # Create an image showing the color palette
                palette_image = Image.new("RGB", (16, 16))
                palette_image.putdata(colors)
                palette_image = palette_image.resize((128, 128), Image.NEAREST)
                palette_tk = ImageTk.PhotoImage(palette_image)
                self.palette_label.config(image=palette_tk)
                self.palette_label.image = palette_tk  # Keep reference

if __name__ == "__main__":
    root = tk.Tk()
    app = PCXViewer(root)
    root.mainloop()
