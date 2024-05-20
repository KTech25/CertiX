from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")
        self.name_input = tk.StringVar()

        self.initialize_directories(['templates', 'certificates', 'fonts'])

        self.templates = []
        self.fonts = []
        self.selected_template = tk.StringVar()
        self.selected_font = tk.StringVar()

        self.load_templates()
        self.load_fonts()
        self.create_widgets()

    def initialize_directories(self, directories):
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")

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

    def add_font(self):
        file_path = filedialog.askopenfilename(title="Select Font", filetypes=[
                                               ("Font files", "*.ttf;*.otf")])
        if file_path:
            dest_path = f"fonts/{os.path.basename(file_path)}"
            shutil.copy(file_path, dest_path)
            self.load_fonts()
            self.update_font_menu()
            self.selected_font.set(f"Selected Font: {dest_path}")

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

    def generate_certificate(self):
        names = self.name_input.get().split(',')
        template_path = self.selected_template.get()
        font_path = self.selected_font.get()

        if "No templates available" in template_path or "No fonts available" in font_path:
            messagebox.showerror(
                "Error", "Please add a template and a font before generating certificates.")
            return

        if not os.path.exists(template_path):
            messagebox.showerror("Error", f"Template file '{
                                 template_path}' does not exist.")
            return

        if not os.path.exists(font_path):
            messagebox.showerror("Error", f"Font file '{
                                 font_path}' does not exist.")
            return

        for name in names:
            name = name.strip()
            try:
                certificate_img = Image.open(template_path)
                draw = ImageDraw.Draw(certificate_img)
                font = ImageFont.truetype(font_path, 100)  # Default font size

                text_position = (
                    (certificate_img.width - draw.textlength(name, font=font)) / 2,
                    (certificate_img.height / 2)-50
                )
                # you can change the text position here
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

    def show_selected_template(self, selected_template):
        if selected_template != "Selected Template: None":
            template_image = Image.open(selected_template)
            template_image.thumbnail((200, 200))
            self.template_photo = ImageTk.PhotoImage(template_image)
            self.selected_template_label.config(image=self.template_photo)
            self.selected_template_label.image = self.template_photo
        else:
            self.selected_template_label.config(image="")

    def show_selected_font(self, selected_font):
        if selected_font != "Selected Font: None":
            # font=selected_font.split("/")[1].split(".")[0]
            font = ImageFont.truetype(selected_font)
            font_name = font.getname()[0]
            print(font_name)
            # print(os.path.splitext(os.path.basename(selected_font))[0])
            self.font_sample_label.config(font=(font_name, 32))

    def load_names_from_excel(self):
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[
                                               ("Excel files", "*.xlsx;*.xls")])
        if file_path:
            df = pd.read_excel(
                file_path, sheet_name='Sheet1', usecols=['Name'])

            if 'Name' in df.columns:
                names = df['Name'].dropna().tolist()
                print(names)
                self.name_input.set(', '.join(names))
            else:
                messagebox.showerror(
                    "Error", "The selected Excel file does not contain a 'Name' column.")

    def create_widgets(self):
        tk.Label(self.root, text="Enter names (comma separated):").grid(
            row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.name_input).grid(
            row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Add Template", command=self.add_template).grid(
            row=1, column=0, padx=10, pady=10)
        self.template_menu = tk.OptionMenu(
            self.root, self.selected_template, *self.templates, command=self.show_selected_template)
        self.template_menu.grid(row=1, column=1, padx=10, pady=10)
        self.selected_template.set("Selected Template: None")

        self.selected_template_label = tk.Label(self.root, text="")
        self.selected_template_label.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Add Font", command=self.add_font).grid(
            row=3, column=0, padx=10, pady=10)
        self.font_menu = tk.OptionMenu(
            self.root, self.selected_font, *self.fonts, command=self.show_selected_font)
        self.font_menu.grid(row=3, column=1, padx=10, pady=10)
        self.selected_font.set("Selected Font: None")

        self.font_sample_label = tk.Label(
            self.root, text="Sample Text", font=("Calibri", 12))
        self.font_sample_label.grid(
            row=4, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self.root, text="Load Names from Excel", command=self.load_names_from_excel).grid(
            row=5, column=0, padx=10, pady=10)

        tk.Button(self.root, text="Generate Certificates", command=self.generate_certificate).grid(
            row=6, column=0, columnspan=2, padx=10, pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGenerator(root)
    root.mainloop()
