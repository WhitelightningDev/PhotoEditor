import os
import subprocess
import threading
import tkinter as tk
from tkinter import Label, Button, filedialog, StringVar, Frame, messagebox
from tkinter import ttk  # For ProgressBar


class RealESRGANApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("900x500")  # Window size
        self.root.config(bg="#F5F5F5")  # Background color

        self.input_file = StringVar()
        self.output_file = StringVar()
        self.dark_mode = False

        # Load custom images
        self.dark_mode_icon = tk.PhotoImage(file="assets/night-mode.png").subsample(4)

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

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", maximum=100)
        self.progress.pack(pady=10)
        self.progress.pack_forget()  # Hide progress bar initially

        # Status bar
        self.status_bar = Label(root, text="Status: Ready", bg="#F5F5F5", font=("Arial", 10))
        self.status_bar.pack(side='bottom', fill='x')

        # Dark mode toggle button at the bottom right
        self.button_dark_mode = Button(root, image=self.dark_mode_icon, command=self.toggle_dark_mode,
                                        bg="#9C27B0", fg="white", font=("Arial", 12, "bold"), relief="flat", padx=10, bd=0)
        self.button_dark_mode.pack(side='bottom', anchor='se', padx=10, pady=10)

        # Bind resizing
        self.root.bind("<Configure>", self.on_resize)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file_path:
            self.input_file.set(file_path)
            output_path = os.path.splitext(file_path)[0] + "_output.png"
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

            processing_thread = threading.Thread(target=self.process_image, args=(output_path,))
            processing_thread.start()

    def process_image(self, output_path):
        input_path = self.input_file.get()
        if input_path:
            # Show the progress bar
            self.progress.pack(pady=10)
            self.progress.start()

            # Run the image processing command
            command = f'"C:\\Users\\DellUser\\IdeaProjects\\PhotoEditor\\realesrgan\\realesrgan-ncnn-vulkan.exe" -i "{input_path}" -o "{output_path}" -s 1'

            try:
                # Execute the command and capture output
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Track progress based on output
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.update_progress(output.strip())

                # Hide the progress bar once done
                self.progress.stop()
                self.progress.pack_forget()

                # Show success message
                self.show_message("Success", f"Image processed and saved as:\n{output_path}")
                self.status_bar.config(text="Status: Ready")

            except Exception as e:
                self.progress.stop()
                self.progress.pack_forget()

                self.show_message("Error", f"An error occurred: {str(e)}")
                self.status_bar.config(text="Status: Error")

    def update_progress(self, output):
        """Update progress bar based on the command output."""
        if output.endswith('%'):
            try:
                percentage = float(output.replace('%', ''))
                self.progress['value'] = percentage  # Update the progress bar value
                self.status_bar.config(text=f"Status: Processing... {percentage}%")  # Update status with percentage
            except ValueError:
                pass  # Handle cases where parsing fails

    def toggle_dark_mode(self):
        """Toggle dark mode on and off."""
        self.dark_mode = not self.dark_mode
        bg_color = "#121212" if self.dark_mode else "#F5F5F5"
        fg_color = "white" if self.dark_mode else "#555"
        title_bg_color = "#6200EE" if not self.dark_mode else "#3700B3"

        self.root.config(bg=bg_color)
        self.title_frame.config(bg=title_bg_color)
        self.title_label.config(bg=title_bg_color, fg="white")
        self.frame.config(bg=bg_color)
        self.io_frame.config(bg=bg_color)
        self.status_bar.config(bg=bg_color, fg=fg_color)

        for widget in self.io_frame.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)

        for widget in self.button_frame.winfo_children():
            widget.config(bg="#6200EE" if self.dark_mode else "#FF9800", fg="white")

    def show_message(self, title, message):
        """Show a message box."""
        self.root.after(0, lambda: messagebox.showinfo(title, message))

    def on_resize(self, event):
        """Adjust widget sizes on window resize."""
        self.frame.config(width=event.width - 40, height=event.height - 100)


if __name__ == "__main__":
    root = tk.Tk()
    app = RealESRGANApp(root)
    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
