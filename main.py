import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import pandas as pd
from mailer import send_certificate

class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator")

        self.selected_template = tk.StringVar()
        self.selected_font = tk.StringVar()
        self.name_input = tk.StringVar()
        self.email_input = tk.StringVar()
        self.course_input = tk.StringVar()
        
        self.text_x_offset = tk.IntVar(value=0)
        self.text_y_offset = tk.IntVar(value=0)
        self.text_x_offset_course = tk.IntVar(value=0)
        self.text_y_offset_course = tk.IntVar(value=0)
        self.font_size = 200
        self.font_size_var = tk.IntVar(value=self.font_size)
        self.include_course_name = tk.BooleanVar()

        self.preview_window = None
        self.course_widgets = []  # To hold widgets for toggling visibility
        
        self.want_to_mail = tk.BooleanVar()
        

        # Checkbox to ask if mailing is needed
        tk.Checkbutton(self.root, text="Do you want to mail the certificate to the students?", variable=self.want_to_mail, command=self.toggle_email_entry).grid(row=11, column=0, columnspan=3, pady=(10, 0))

        
        # Email input field (initially hidden)
        self.email_label = tk.Label(self.root, text="Emails (comma-separated):")
        self.email_entry = tk.Entry(self.root, textvariable=self.email_input, width=40)





        # Template
        tk.Label(self.root, text="Template Image:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.selected_template, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_template).grid(row=0, column=2)

        # Font
        tk.Label(self.root, text="Font File:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.selected_font, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_font).grid(row=1, column=2)

        # Names
        tk.Label(self.root, text="Names (comma-separated):").grid(row=2, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.name_input, width=40).grid(row=2, column=1)

        tk.Button(self.root, text="Load from File", command=self.load_names_from_file).grid(row=2, column=2)

        # Checkbox for course name
        tk.Checkbutton(self.root, text="Do you want to write course name as well?",
                       variable=self.include_course_name, command=self.toggle_course_fields).grid(row=3, column=0, columnspan=3)

        # Course name field
        lbl_course = tk.Label(self.root, text="Course Name:")
        entry_course = tk.Entry(self.root, textvariable=self.course_input, width=40)
        self.course_widgets.extend([lbl_course, entry_course])
        lbl_course.grid(row=4, column=0, sticky="e")
        entry_course.grid(row=4, column=1)

        # Text offset for name
        tk.Label(self.root, text="X Offset for Name:").grid(row=5, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_x_offset, width=10).grid(row=5, column=1, sticky="w")
        tk.Label(self.root, text="Y Offset for Name:").grid(row=6, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.text_y_offset, width=10).grid(row=6, column=1, sticky="w")

        # Offset for course name
        lbl_x_course = tk.Label(self.root, text="X Offset for Course:")
        entry_x_course = tk.Entry(self.root, textvariable=self.text_x_offset_course, width=10)
        lbl_y_course = tk.Label(self.root, text="Y Offset for Course:")
        entry_y_course = tk.Entry(self.root, textvariable=self.text_y_offset_course, width=10)
        self.course_widgets.extend([lbl_x_course, entry_x_course, lbl_y_course, entry_y_course])
        lbl_x_course.grid(row=7, column=0, sticky="e")
        entry_x_course.grid(row=7, column=1, sticky="w")
        lbl_y_course.grid(row=8, column=0, sticky="e")
        entry_y_course.grid(row=8, column=1, sticky="w")

        # Font size
        tk.Label(self.root, text="Font Size:").grid(row=9, column=0, sticky="e")
        self.font_size_entry = tk.Entry(self.root, textvariable=self.font_size_var, width=5)
        self.font_size_entry.grid(row=9, column=1)
        tk.Button(self.root, text="+", width=3, command=self.increase_font_size).grid(row=9, column=2, sticky="w")
        tk.Button(self.root, text="-", width=3, command=self.decrease_font_size).grid(row=9, column=2, sticky="e")
        self.font_size_entry.bind("<Return>", self.update_font_size_from_entry)

        # Buttons
        tk.Button(self.root, text="Generate Certificates", command=self.generate_certificates).grid(row=10, column=0, columnspan=2)
        tk.Button(self.root, text="Live Preview", command=self.show_live_preview).grid(row=10, column=2)

        # Initially hide course fields
        self.toggle_course_fields()

    def toggle_email_entry(self):
        if self.want_to_mail.get():
            self.email_label.grid(row=12, column=0, sticky="e")
            self.email_entry.grid(row=12, column=1)
            
        else:
            self.email_label.grid_remove()
            self.email_entry.grid_remove()

    def toggle_course_fields(self):
        for widget in self.course_widgets:
            if self.include_course_name.get():
                widget.grid()
            else:
                widget.grid_remove()

    def browse_template(self):
        file_path = filedialog.askopenfilename(title="Select Template Image", filetypes=[("Image files", ".png;.jpg;*.jpeg")])
        if file_path:
            self.selected_template.set(file_path)

    def browse_font(self):
        file_path = filedialog.askopenfilename(title="Select Font File", filetypes=[("Font files", "*.ttf")])
        if file_path:
            self.selected_font.set(file_path)

    def increase_font_size(self):
        self.font_size += 1
        self.font_size_var.set(self.font_size)
        self.show_live_preview()

    def decrease_font_size(self):
        if self.font_size > 1:
            self.font_size -= 1
            self.font_size_var.set(self.font_size)
            self.show_live_preview()

    def update_font_size_from_entry(self, event=None):
        try:
            new_size = int(self.font_size_var.get())
            if new_size > 0:
                self.font_size = new_size
                self.show_live_preview()
            else:
                messagebox.showwarning("Invalid Input", "Font size must be greater than 0.")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")

    def load_names_from_file(self):
        file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel files", ".xlsx;.xls")])
        if file_path:
            try:
                # Read the Excel file
                df = pd.read_excel(file_path)

                # Check if the required columns are in the Excel file
                if 'Names' in df.columns and 'Email' in df.columns:
                    # Store the details in an array of objects
                    self.student_details = [{'name': row['Names'], 'email': row['Email']} for _, row in df.iterrows()]
                    
                    # Display the names and emails as a comma-separated string in the input field
                    self.name_input.set(', '.join(df['Names'].tolist()))
                    
                    if self.want_to_mail.get():
                        self.email_input.set(', '.join(df['Email'].tolist()))

                    messagebox.showinfo("Names Loaded", "Names and emails have been successfully loaded from the Excel file.")
                else:
                    messagebox.showerror("Error", "The Excel file must contain 'Names' and 'email' columns.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

    def generate_certificates(self):
        if not self.selected_template.get() or not self.selected_font.get():
            messagebox.showerror("Error", "Please select a template image and a font file.")
            return

        # Check if student details are loaded
        if not hasattr(self, 'student_details') or not self.student_details:
            messagebox.showerror("Error", "Please load the names and emails from the file.")
            return

        for student in self.student_details:
            name = student['name']
            email = student['email']
            
            # Use the course name if selected
            course_name = self.course_input.get() if self.include_course_name.get() else ""

            try:
                # Open template image
                template_img = Image.open(self.selected_template.get())
                draw = ImageDraw.Draw(template_img)
                font = ImageFont.truetype(self.selected_font.get(), self.font_size)

                # Calculate name position
                name_position = (
                    (template_img.width - draw.textlength(name, font=font)) / 2 + self.text_x_offset.get(),
                    (template_img.height / 2) + self.text_y_offset.get()
                )
                draw.text(name_position, name, fill="black", font=font)

                # If course name is included, draw the course name
                if self.include_course_name.get():
                    course_position = (
                        (template_img.width - draw.textlength(course_name, font=font)) / 2 + self.text_x_offset_course.get(),
                        name_position[1] + 80 + self.text_y_offset_course.get()
                    )
                    draw.text(course_position, course_name, fill="black", font=font)

                # Create the 'generated_certificates' folder if it doesn't exist
                os.makedirs("generated_certificates", exist_ok=True)

                # Save the generated certificate as PNG
                certificate_path = f"generated_certificates/{name}.png"
                template_img.save(certificate_path)

                
                if self.want_to_mail.get():
                    send_certificate(email, name, certificate_path)
                    pass
                    

            except Exception as e:
                messagebox.showerror("Error", f"Error generating certificate for {name}: {e}")
                return

        messagebox.showinfo("Success", "Certificates generated successfully!")


    def show_live_preview(self, event=None):
        if not self.selected_template.get() or not self.selected_font.get():
            return

        if self.preview_window is None or not self.preview_window.winfo_exists():
            self.preview_window = Toplevel(self.root)
            self.preview_window.title("Live Preview")
            self.preview_label = tk.Label(self.preview_window)
            self.preview_label.pack()

        try:
            template_img = Image.open(self.selected_template.get())
            draw = ImageDraw.Draw(template_img)
            font = ImageFont.truetype(self.selected_font.get(), self.font_size)

            name = self.name_input.get().split(',')[0].strip()
            name_position = (
                (template_img.width - draw.textlength(name, font=font)) / 2 + self.text_x_offset.get(),
                (template_img.height / 2) + self.text_y_offset.get()
            )
            draw.text(name_position, name, fill="black", font=font)

            if self.include_course_name.get():
                course_name = self.course_input.get().strip()
                course_position = (
                    (template_img.width - draw.textlength(course_name, font=font)) / 2 + self.text_x_offset_course.get(),
                    name_position[1] + 80 + self.text_y_offset_course.get()
                )
                draw.text(course_position, course_name, fill="black", font=font)

            template_img.thumbnail((800, 600), Image.Resampling.LANCZOS)
            preview_img = ImageTk.PhotoImage(template_img)
            self.preview_label.config(image=preview_img)
            self.preview_label.image = preview_img

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the live preview: {e}")

root = tk.Tk()
app = CertificateGenerator(root)
root.mainloop()
