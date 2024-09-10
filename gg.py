import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pandas as pd

class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")
        self.name_input = tk.StringVar()

        self.text_x_offset = 50
        self.text_y_offset = 50
        self.font_size = 20

        self.font_sample_text = "Sample Text"
        self.preview_window = None
        self.current_template_image = None
        self.img_tk = None

        # Creating widgets
        self.create_widgets()

    def create_widgets(self):
        # Entry widget for name input
        tk.Entry(self.root, textvariable=self.name_input).pack()

        # Button to load CSV file
        tk.Button(self.root, text="Load CSV", command=self.load_csv).pack()

        # Button to open preview window
        tk.Button(self.root, text="Open Preview", command=self.open_preview).pack()

        # Buttons to increase/decrease font size
        tk.Button(self.root, text="Increase Font Size", command=self.increase_font_size).pack()
        tk.Button(self.root, text="Decrease Font Size", command=self.decrease_font_size).pack()

    def load_csv(self):
        file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = pd.read_csv(file_path)
            print(data['Name'].tolist())  # Assume there's a 'Name' column in the CSV

    def open_preview(self):
        # Open a new window for the live preview
        if self.preview_window is None or not self.preview_window.winfo_exists():
            self.preview_window = tk.Toplevel(self.root)
            self.preview_window.geometry("400x400")
            self.preview_canvas = tk.Canvas(self.preview_window, width=400, height=400)
            self.preview_canvas.pack()

            self.load_template()
            self.preview_text()

            # Bind arrow keys to move text
            self.preview_window.bind("<Left>", self.move_left)
            self.preview_window.bind("<Right>", self.move_right)
            self.preview_window.bind("<Up>", self.move_up)
            self.preview_window.bind("<Down>", self.move_down)

    def load_template(self):
        # Load a blank image or template (placeholder for demonstration)
        self.current_template_image = Image.new("RGB", (400, 400), color="white")
        self.update_preview()

    def update_preview(self):
        # Clear the canvas first
        self.preview_canvas.delete("all")

        # Create a new blank image
        self.current_template_image = Image.new("RGB", (400, 400), color="white")
        draw = ImageDraw.Draw(self.current_template_image)

        # Set the font with the current font size
        font = ImageFont.truetype("arial.ttf", self.font_size)

        # Draw text at the current x and y offsets
        draw.text((self.text_x_offset, self.text_y_offset), self.font_sample_text, font=font, fill="black")

        # Update the canvas with the new image
        self.img_tk = ImageTk.PhotoImage(self.current_template_image)
        self.preview_canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def preview_text(self):
        # Create initial text for preview
        self.update_preview()

    # Arrow key movement methods
    def move_left(self, event):
        self.text_x_offset -= 10
        self.update_preview()

    def move_right(self, event):
        self.text_x_offset += 10
        self.update_preview()

    def move_up(self, event):
        self.text_y_offset -= 10
        self.update_preview()

    def move_down(self, event):
        self.text_y_offset += 10
        self.update_preview()

    # Font size adjustment methods
    def increase_font_size(self):
        self.font_size += 2
        self.update_preview()

    def decrease_font_size(self):
        self.font_size -= 2
        self.update_preview()

# Main window setup
root = tk.Tk()
app = CertificateGenerator(root)
root.mainloop()
