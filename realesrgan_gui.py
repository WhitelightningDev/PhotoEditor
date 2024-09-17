import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import Label, Button, filedialog, StringVar, Frame, messagebox
from tkinter import ttk  # For ProgressBar
from pdf2image import convert_from_path


class RealESRGANApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor - WhiteLightningDev")
        self.root.geometry("900x500")  # Window size
        self.root.config(bg="#F5F5F5")  # Background color

        self.input_file = StringVar()
        self.output_file = StringVar()
        self.dark_mode = False

        # Load custom images
        self.dark_mode_icon = tk.PhotoImage(file=self.resource_path("assets/night-mode.png")).subsample(5)

        # Create a title frame
        self.title_frame = Frame(root, bg="#6200EE", bd=0,
                                 highlightbackground="#6200EE", highlightcolor="#6200EE", highlightthickness=2)
        self.title_frame.pack(fill='x')

        self.title_label = Label(self.title_frame,
                                 text="Image Processor Powered by Real-ESRGAN",
                                 bg="#6200EE", fg="white", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=15)

        # Create a main frame for better organization
        self.frame = Frame(root, bg="#F5F5F5", bd=0,
                           highlightbackground="#6200EE", highlightcolor="#6200EE", highlightthickness=2)
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Input and Output Frame
        self.io_frame = Frame(self.frame, bg="#F5F5F5")
        self.io_frame.pack(pady=10, fill='x')

        # Input file label and entry
        self.label_input = Label(self.io_frame, text="Input File:", bg="#F5F5F5", font=("Arial", 12))
        self.label_input.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.label_input_file = Label(self.io_frame, textvariable=self.input_file, bg="#F5F5F5",
                                       font=("Arial", 10), fg="#555")
        self.label_input_file.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Output file label
        self.label_output = Label(self.io_frame, text="Output File:", bg="#F5F5F5", font=("Arial", 12))
        self.label_output.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.label_output_file = Label(self.io_frame, textvariable=self.output_file, bg="#F5F5F5",
                                       font=("Arial", 10), fg="#555")
        self.label_output_file.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Create a button frame
        self.button_frame = Frame(self.frame, bg="#F5F5F5")
        self.button_frame.pack(pady=20)

        # Load button
        self.button_load = Button(self.button_frame, text="Load Image", command=self.load_image,
                                  bg="#6200EE", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, bd=0)
        self.button_load.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        # Process button
        self.button_process = Button(self.button_frame, text="Process Image", command=self.start_processing,
                                     bg="#FF9800", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, bd=0)
        self.button_process.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Check Progress button
        self.button_check_progress = Button(self.button_frame, text="Check Progress", command=self.check_progress,
                                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, bd=0)
        self.button_check_progress.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        # Cancel button
        self.button_cancel = Button(self.button_frame, text="Cancel", command=self.cancel_processing,
                                    bg="#F44336", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, bd=0)
        self.button_cancel.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", maximum=100)
        self.progress.pack(pady=10)
        self.progress.pack_forget()  # Hide progress bar initially

        # Status bar
        self.status_bar = Label(root, text="Status: Ready", bg="#F5F5F5", font=("Arial", 10))
        self.status_bar.pack(side='bottom', fill='x')



        # Bind resizing
        self.root.bind("<Configure>", self.on_resize)

        self.processing_thread = None  # Track processing thread

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Image files", "*.jpg *.png *.pdf"),
            ("HTML files", "*.html *.htm"),
            ("All files", "*.*")
        ])

        if file_path:
            self.input_file.set(file_path)

            if file_path.lower().endswith('.pdf'):
                # If the input is a PDF, convert it to an image
                self.process_pdf(file_path)

            elif file_path.lower().endswith(('.html', '.htm')):
                # If the input is an HTML file, convert it to PDF first
                pdf_path = self.convert_html_to_pdf(file_path)
                if pdf_path:
                    self.process_pdf(pdf_path)

            else:
                # For image files
                output_path = os.path.splitext(file_path)[0] + "_output.png"
                self.output_file.set(output_path)


    def process_pdf(self, pdf_path):
        """Process the PDF and convert its pages to images."""
        images = convert_from_path(pdf_path)  # Use convert_from_path
        self.temp_image_paths = []  # Store temporary image paths
        for i, image in enumerate(images):
            temp_image_path = f"temp_image_{i}.png"  # Temporary path for each page
            image.save(temp_image_path, "PNG")  # Save each page as PNG
            self.temp_image_paths.append(temp_image_path)
        # Set the output file for the first page processed
        output_path = os.path.splitext(pdf_path)[0] + "_output.png"
        self.output_file.set(output_path)

    def start_processing(self):
        """Starts the image processing in a new thread."""
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Output Image"
        )
        if output_path:  # If the user selects a location
            self.output_file.set(output_path)  # Update output path
            self.status_bar.config(text="Status: Processing...")

            self.processing_thread = threading.Thread(target=self.process_image, args=(output_path,))
            self.processing_thread.start()
    def cancel_processing(self):
        """Cancel the processing thread."""
        if self.processing_thread and self.processing_thread.is_alive():
            # Here we would need to properly terminate the process.
            # This is a placeholder for termination logic.
            self.status_bar.config(text="Status: Canceled")
            self.progress.stop()
            self.progress.pack_forget()
            self.processing_thread = None

    def check_progress(self):
        """Open a terminal to show processing output."""
        input_path = self.input_file.get()
        if input_path:
            terminal_command = f'cmd /c "{self.resource_path("realesrgan/realesrgan-ncnn-vulkan.exe")}" -i "{input_path}"'
            subprocess.Popen(terminal_command, shell=True)

    def resource_path(self, relative_path):
        """ Get the absolute path to a resource, works for both dev and PyInstaller """
        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temp folder for resources
        except AttributeError:
            base_path = os.path.abspath(".")  # Fall back to current directory in development mode
        return os.path.join(base_path, relative_path)

    def process_image(self, output_path):
        input_path = self.input_file.get()
        if input_path:
            # Show the progress bar
            self.progress.pack(pady=10)
            self.progress.start()

            # Get the correct path for the Real-ESRGAN executable
            executable_path = self.resource_path('realesrgan/realesrgan-ncnn-vulkan.exe')

            # Construct the command with the model name
            command = f'"{executable_path}" -i "{input_path}" -o "{output_path}" -n realesrgan-x4plus'

            try:
                # Execute the command and capture output and errors
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           text=True)

                # Log the Real-ESRGAN output
                for line in process.stdout:
                    print(line.strip())  # Replace with actual progress handling

                process.wait()  # Wait for the process to finish

                self.show_message("Success", f"Image processed and saved as:\n{output_path}")
                self.status_bar.config(text="Status: Done")
            except Exception as e:
                self.show_message("Exception", str(e))
                self.status_bar.config(text="Status: Error")

            self.update_progress()  # Update progress (you may need to adjust this)

    def update_progress(self):
        """Update the progress based on the output."""
        # This method should be implemented to interpret output messages for actual progress tracking
        # This is a placeholder for progress update logic
        self.progress.stop()
        self.progress.pack_forget()  # Hide the progress bar when done

    def show_message(self, title, message):
        """Show a message box."""
        messagebox.showinfo(title, message)



    def on_resize(self, event):
        """Adjust layout on resize."""
        width = event.width
        height = event.height
        # You can adjust the sizes of widgets here if necessary


if __name__ == "__main__":
    root = tk.Tk()
    app = RealESRGANApp(root)
    root.mainloop()
