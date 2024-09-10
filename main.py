from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import pandas as pd

class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")
        self.name_input = tk.StringVar()

        self.initialize_directories(['templates', 'certificates', 'fonts'])

        self.templates = []
        self.fonts = []
        self.font_size = 80
        self.selected_template = tk.StringVar()
        self.selected_font = tk.StringVar()

        self.load_templates()
        self.load_fonts()
        self.create_widgets()
        

        # Variables for text position adjustment
        self.text_x_offset = tk.IntVar(value=0)
        self.text_y_offset = tk.IntVar(value=0)
        
        # Live preview window
        self.preview_window = None
        self.preview_label = None
        self.current_template_image = None
        self.font_sample_text = "Sample Text"

    def initialize_directories(self, directories):
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
    
    def create_widgets(self):
        tk.Label(self.root, text="Enter names (comma separated):").grid(
            row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root, textvariable=self.name_input)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="Load Names from Excel", command=self.load_names_from_file).grid(
            row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Add Template", command=self.add_template).grid(
            row=2, column=0, padx=10, pady=10)
        self.template_menu = tk.OptionMenu(
            self.root, self.selected_template, *self.templates, command=self.show_live_preview)
        self.template_menu.grid(row=2, column=1, padx=10, pady=10)
        self.selected_template.set("Selected Template: None")

        self.selected_template_label = tk.Label(self.root, text="")
        self.selected_template_label.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Add Font", command=self.add_font).grid(
            row=3, column=0, padx=10, pady=10)
        self.font_menu = tk.OptionMenu(
            self.root, self.selected_font, *self.fonts, command=self.show_live_preview)
        self.font_menu.grid(row=3, column=1, padx=10, pady=10)
        
        tk.Label(self.root, text="Adjust Font Size:").grid(
            row=4, column=0, columnspan=2, padx=10, pady=10)
        
        tk.Button(self.root, text="Increase Font Size", command=lambda: self.increase_font_size()).grid(
            row=6, column=1, columnspan=1, padx=10, pady=10)
        self.font_size_label = tk.Label(self.root, text=f"{self.font_size}")
        self.font_size_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Decrease Font Size", command=lambda: self.decrease_font_size()).grid(
            row=6, column=0, columnspan=1, padx=10, pady=10)


        tk.Label(self.root, text="Adjust Text Position:").grid(
            row=7, column=0, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Up", command=lambda: self.shift_text('up')).grid(
            row=8, column=0,columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Down", command=lambda: self.shift_text('down')).grid(
            row=10, column=0,columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Left", command=lambda: self.shift_text('left')).grid(
            row=9, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Right", command=lambda: self.shift_text('right')).grid(
            row=9, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Generate Certificates", command=self.generate_certificate).grid(
            row=11, column=0, columnspan=2, padx=10, pady=10)

        
    def load_templates(self):
        self.templates = [f"templates/{file}" for file in os.listdir(
            'templates') if file.endswith(('.png', '.jpg', '.jpeg'))]
        if self.templates:
            self.selected_template.set(self.templates[0])
        else:
            self.templates = ["No templates available"]
            self.selected_template.set(self.templates[0])

    def load_fonts(self):
        self.fonts = [
            f"fonts/{file}" for file in os.listdir('fonts') if file.endswith(('.ttf', '.otf'))]
        if self.fonts:
            self.selected_font.set(self.fonts[0])
        else:
            self.fonts = ["No fonts available"]
            self.selected_font.set(self.fonts[0])

    def add_template(self):
        file_path = filedialog.askopenfilename(title="Select Template", filetypes=[
                                               ("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            dest_path = f"templates/{os.path.basename(file_path)}"
            shutil.copy(file_path, dest_path)
            self.load_templates()
            self.update_template_menu()
            self.selected_template.set(f"Selected Template: {dest_path}")
            self.selected_template_label.config(
                text=f"Selected Template: {dest_path}")
            self.show_live_preview()

    def add_font(self):
        file_path = filedialog.askopenfilename(title="Select Font", filetypes=[
                                               ("Font files", "*.ttf;*.otf")])
        if file_path:
            dest_path = f"fonts/{os.path.basename(file_path)}"
            shutil.copy(file_path, dest_path)
            self.load_fonts()
            self.update_font_menu()
            self.selected_font.set(f"Selected Font: {dest_path}")
            self.show_live_preview()

    def update_template_menu(self):
        menu = self.template_menu["menu"]
        menu.delete(0, "end")
        for template in self.templates:
            menu.add_command(
                label=template, command=lambda value=template: self.selected_template.set(value))

    def update_font_menu(self):
        menu = self.font_menu["menu"]
        menu.delete(0, "end")
        for font in self.fonts:
            menu.add_command(
                label=font, command=lambda value=font: self.selected_font.set(value))

    def shift_text(self, direction):
        print(direction)
        if direction == 'up':
            self.text_y_offset.set(self.text_y_offset.get() - 10)
        elif direction == 'down':
            self.text_y_offset.set(self.text_y_offset.get() + 10)
        elif direction == 'left':
            self.text_x_offset.set(self.text_x_offset.get() - 10)
        elif direction == 'right':
            self.text_x_offset.set(self.text_x_offset.get() + 10)
        else:
            print("invalid direction")
        self.show_live_preview()

    def generate_certificate(self):
        names = self.name_input.get().split(',')
        template_path = self.selected_template.get()
        font_path = self.selected_font.get()

        if "No templates available" in template_path or "No fonts available" in font_path:
            messagebox.showerror(
                "Error", "Please add a template and a font before generating certificates.")
            return

        if not os.path.exists(template_path):
            messagebox.showerror("Error", f"Template file '{template_path}' does not exist.")
            return

        if not os.path.exists(font_path):
            messagebox.showerror("Error", f"Font file '{font_path}' does not exist.")
            return

        for name in names:
            name = name.strip()
            try:
                certificate_img = Image.open(template_path)
                draw = ImageDraw.Draw(certificate_img)
                font = ImageFont.truetype(font_path, self.font_size)  # Default font size

                text_position = (
                    (certificate_img.width - draw.textlength(name, font=font)) / 2 + self.text_x_offset.get(),
                    (certificate_img.height / 2)-50 + self.text_y_offset.get()
                )
                draw.text(text_position, name, fill="black", font=font)

                if not os.path.exists('certificates'):
                    os.makedirs('certificates')

                certificate_img.save(f"certificates/{name}_certificate.png")
                print(f"Certificate for '{name}' generated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        messagebox.showinfo(
            "Success", "All certificates have been generated successfully!")
        os.startfile('certificates')
        self.name_entry.config(textvariable="")
    
    def increase_font_size(self):
        print("increase")
        self.font_size += 2
        self.update_font_size_label()
        self.show_live_preview()

    def decrease_font_size(self):
        if self.font_size > 10:  # Ensure font size doesn't go below a minimum value
            self.font_size -= 2
            self.update_font_size_label()
            self.show_live_preview()
    
    def update_font_size_label(self):
        self.font_size_label.config(text=f"{self.font_size}")
    
    def show_live_preview(self,*args):
        window_width = 600
        window_height = 400
        if not self.preview_window:
            self.preview_window = Toplevel(self.root)
            self.preview_window.title("Live Preview")
            self.preview_window.geometry(f"{window_width}x{window_height}") 
            
            # Fixed window size
            self.preview_window.bind("<Left>", lambda event: self.shift_text('left'))
            self.preview_window.bind("<Right>", lambda event: self.shift_text('right'))
            self.preview_window.bind("<Up>", lambda event: self.shift_text('up'))
            self.preview_window.bind("<Down>", lambda event: self.shift_text('down'))
            self.root.bind("<KP_Add>",lambda event: self.increase_font_size)  # For the numpad + key
            self.root.bind("<plus>",lambda event: self.increase_font_size)    # For the main + key
            self.root.bind("<minus>",lambda event: self.decrease_font_size)   # For the main - key
            self.root.bind("<KP_Subtract>",lambda event: self.decrease_font_size)
            
            
            self.preview_label = tk.Label(self.preview_window)
            self.preview_label.pack(fill=tk.BOTH, expand=True)

        # Load template image
        template_path = self.selected_template.get()
        if os.path.exists(template_path):
            template_img = Image.open(template_path)
            draw = ImageDraw.Draw(template_img)

            # Load selected font
            font_path = self.selected_font.get()
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, self.font_size)
                except Exception as e:
                    print(f"Failed to load font: {e}")
                    font = ImageFont.load_default()

                # Calculate text position with offsets
                text_position = (
                    (template_img.width - draw.textlength(self.font_sample_text, font=font)) / 2 + self.text_x_offset.get(),
                    (template_img.height / 2) - 50 + self.text_y_offset.get()
                )

                # Draw the sample text on the template image
                draw.text(text_position, self.font_sample_text, fill="black", font=font)

            # Resize the image to fit the width of the window
            img_width, img_height = template_img.size
            aspect_ratio = img_width / img_height

            new_width = window_width
            new_height = int(new_width / aspect_ratio)

            # Ensure the new height does not exceed the window height
            if new_height > window_height:
                new_height = window_height
                new_width = int(new_height * aspect_ratio)

            # Resize the image
            resized_img = template_img.resize((new_width, new_height), Image.ANTIALIAS)

            # Convert to ImageTk for displaying in Tkinter
            self.current_template_image = ImageTk.PhotoImage(resized_img)
            self.preview_label.config(image=self.current_template_image)
            self.preview_label.image = self.current_template_image

    def load_names_from_file(self):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=[
                                               ("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path, sheet_name='Sheet1', usecols=['Name'])
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, usecols=['Name'])
        else:
            messagebox.showerror("Error", "Unsupported file type.")
            return

        if 'Name' in df.columns:
            names = df['Name'].dropna().tolist()
            print(names)
            self.name_input.set(', '.join(names))
        else:
            messagebox.showerror(
                "Error", "The selected file does not contain a 'Name' column.")

   


if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGenerator(root)
    root.mainloop()
