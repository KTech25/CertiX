import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import pandas as pd

class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")

        self.selected_template = tk.StringVar()
        self.selected_font = tk.StringVar()
        self.name_input = tk.StringVar()
        self.course_input = tk.StringVar()

        # Offsets for positioning the text
        self.text_x_offset_name = tk.IntVar(value=0)
        self.text_y_offset_name = tk.IntVar(value=0)
        self.text_x_offset_course = tk.IntVar(value=0)
        self.text_y_offset_course = tk.IntVar(value=0)

        # Font size for name and course
        self.font_size_name = 40
        self.font_size_course = 30

        self.preview_window = None

        # User Interface
        tk.Label(self.root, text="Template Image:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.selected_template, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_template).grid(row=0, column=2)

        tk.Label(self.root, text="Font File:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.selected_font, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_font).grid(row=1, column=2)

        tk.Label(self.root, text="Names (comma-separated):").grid(row=2, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.name_input, width=40).grid(row=2, column=1)
        tk.Button(self.root, text="Load from File", command=self.load_names_from_file).grid(row=2, column=2)

        tk.Label(self.root, text="Course Name:").grid(row=3, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.course_input, width=40).grid(row=3, column=1)

        # Text position controls for Name
        tk.Label(self.root, text="X Offset for Name:").grid(row=4, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_x_offset_name, width=10).grid(row=4, column=1, sticky="w")
        tk.Label(self.root, text="Y Offset for Name:").grid(row=5, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_y_offset_name, width=10).grid(row=5, column=1, sticky="w")

        # Text position controls for Course
        tk.Label(self.root, text="X Offset for Course:").grid(row=6, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_x_offset_course, width=10).grid(row=6, column=1, sticky="w")
        tk.Label(self.root, text="Y Offset for Course:").grid(row=7, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_y_offset_course, width=10).grid(row=7, column=1, sticky="w")

        # Font size controls
        tk.Button(self.root, text="Increase Name Font Size", command=self.increase_font_size_name).grid(row=8, column=0, sticky="w")
        tk.Button(self.root, text="Decrease Name Font Size", command=self.decrease_font_size_name).grid(row=8, column=1, sticky="e")
        
        tk.Button(self.root, text="Increase Course Font Size", command=self.increase_font_size_course).grid(row=9, column=0, sticky="w")
        tk.Button(self.root, text="Decrease Course Font Size", command=self.decrease_font_size_course).grid(row=9, column=1, sticky="e")

        self.font_size_name_label = tk.Label(self.root, text=f"Name Font Size: {self.font_size_name}")
        self.font_size_name_label.grid(row=8, column=2)

        self.font_size_course_label = tk.Label(self.root, text=f"Course Font Size: {self.font_size_course}")
        self.font_size_course_label.grid(row=9, column=2)

        # Generate and preview buttons
        tk.Button(self.root, text="Generate Certificates", command=self.generate_certificates).grid(row=10, column=0, columnspan=2)
        tk.Button(self.root, text="Live Preview", command=self.show_live_preview).grid(row=10, column=2)

    def browse_template(self):
        file_path = filedialog.askopenfilename(title="Select Template Image", filetypes=[("Image files", ".png;.jpg;*.jpeg")])
        if file_path:
            self.selected_template.set(file_path)

    def browse_font(self):
        file_path = filedialog.askopenfilename(title="Select Font File", filetypes=[("Font files", "*.ttf")])
        if file_path:
            self.selected_font.set(file_path)

    def generate_certificates(self):
        if not self.selected_template.get() or not self.selected_font.get():
            messagebox.showerror("Error", "Please select a template image and a font file.")
            return

        # Split the names and course names into lists
        names = self.name_input.get().split(',')
        course_names = self.course_input.get().split(',')

        if len(names) != len(course_names):
            messagebox.showerror("Error", "The number of names and course names do not match.")
            return

        for name, course_name in zip(names, course_names):
            try:
                name = name.strip()
                course_name = course_name.strip()

                # Load the template image
                template_img = Image.open(self.selected_template.get())
                draw = ImageDraw.Draw(template_img)

                # Load the fonts for name and course
                font_name = ImageFont.truetype(self.selected_font.get(), self.font_size_name)
                font_course = ImageFont.truetype(self.selected_font.get(), self.font_size_course)

                # Calculate position for the name
                name_width, name_height = draw.textbbox((0, 0), name, font=font_name)[2:4]
                name_position = (
                    (template_img.width - name_width) / 2 + self.text_x_offset_name.get(),
                    (template_img.height / 2) + self.text_y_offset_name.get()
                )

                # Calculate position for the course name (below the name)
                course_width, course_height = draw.textbbox((0, 0), course_name, font=font_course)[2:4]
                course_position = (
                    (template_img.width - course_width) / 2 + self.text_x_offset_course.get(),
                    name_position[1] + name_height + self.text_y_offset_course.get()
                )

                # Draw the name and course on the template
                draw.text(name_position, name, fill="black", font=font_name)
                draw.text(course_position, course_name, fill="black", font=font_course)

                # Save the generated certificate
                output_dir = "generated_certificates"
                os.makedirs(output_dir, exist_ok=True)
                template_img.save(f"{output_dir}/{name}_certificate.png")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while generating certificate for {name}: {e}")
                return

        messagebox.showinfo("Success", "Certificates generated successfully!")
    
    def load_names_from_file(self):
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", ".xlsx;.xls")])
        if file_path:
            df = pd.read_excel(file_path)
            print(df.columns)
            if 'Names' in df.columns:
                self.name_input.set(', '.join(df['Names'].tolist()))
                messagebox.showinfo("Names Loaded", "Names have been successfully loaded from the Excel file.")
            else:
                messagebox.showerror("Error", "The Excel file does not contain a 'Names' column.")
            
            if 'Course' in df.columns:
                self.course_input.set(', '.join(df['Course'].tolist()))
                messagebox.showinfo("Course Loaded", "Course have been successfully loaded from the Excel file.")
            else:
                messagebox.showerror("Error", "The Excel file does not contain a 'Names' column.")

    def increase_font_size_name(self):
        self.font_size_name += 2
        self.font_size_name_label.config(text=f"Name Font Size: {self.font_size_name}")
        # self.show_live_preview()

    def decrease_font_size_name(self):
        self.font_size_name -= 2
        self.font_size_name_label.config(text=f"Name Font Size: {self.font_size_name}")
        # self.show_live_preview()

    def increase_font_size_course(self):
        self.font_size_course += 2
        self.font_size_course_label.config(text=f"Course Font Size: {self.font_size_course}")
        # self.show_live_preview()

    def decrease_font_size_course(self):
        self.font_size_course -= 2
        self.font_size_course_label.config(text=f"Course Font Size: {self.font_size_course}")
        # self.show_live_preview()

    def show_live_preview(self):
        if not self.selected_template.get() or not self.selected_font.get():
            return

        if self.preview_window is None or not self.preview_window.winfo_exists():
            self.preview_window = Toplevel(self.root)
            self.preview_window.title("Live Preview")
            self.preview_label = tk.Label(self.preview_window)
            self.preview_label.pack()

        try:
            # Load the template and create a live preview
            template_img = Image.open(self.selected_template.get())
            draw = ImageDraw.Draw(template_img)
            font_name = ImageFont.truetype(self.selected_font.get(), self.font_size_name)
            font_course = ImageFont.truetype(self.selected_font.get(), self.font_size_course)

            # Preview Name
            name = self.name_input.get().split(',')[0].strip()  # Preview the first name
            name_position = (
                (template_img.width - draw.textbbox((0, 0), name, font=font_name)[2]) / 2 + self.text_x_offset_name.get(),
                (template_img.height / 2) + self.text_y_offset_name.get()
            )
            draw.text(name_position, name, fill="black", font=font_name)

            # Preview Course Name
            course_name = self.course_input.get().split(',')[0].strip()
            course_position = (
                (template_img.width - draw.textbbox((0, 0), course_name, font=font_course)[2]) / 2 + self.text_x_offset_course.get(),
                name_position[1] + 80 + self.text_y_offset_course.get()
            )
            draw.text(course_position, course_name, fill="black", font=font_course)

            # Display preview
            preview_img = ImageTk.PhotoImage(template_img)
            self.preview_label.config(image=preview_img)
            self.preview_label.image = preview_img  # Keep reference to avoid garbage collection

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the live preview: {e}")


root = tk.Tk()
app = CertificateGenerator(root)
root.mainloop()
