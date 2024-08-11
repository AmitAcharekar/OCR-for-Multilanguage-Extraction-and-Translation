import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageCropperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.image = None
        self.image_on_canvas = None
        self.cropped_image = None

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.crop_button = tk.Button(root, text="Crop Image", command=self.crop_image)
        self.crop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select an image file.")
            return

        try:
            self.image = Image.open(file_path)
            self.image.thumbnail((800, 600), Image.Resampling.LANCZOS)  # Resize keeping aspect ratio
            self.image_on_canvas = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.image_on_canvas, anchor=tk.NW)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        pass

    def crop_image(self):
        if not self.image or not self.rect:
            messagebox.showwarning("Warning", "Please select an area to crop.")
            return

        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if x1 == x2 or y1 == y2:
            messagebox.showwarning("Warning", "Please select a valid area to crop.")
            return

        self.cropped_image = self.image.crop((x1, y1, x2, y2))
        self.cropped_image.show()

    def save_image(self):
        if self.cropped_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                self.cropped_image.save(save_path)
                messagebox.showinfo("Success", f"Image saved to {save_path}")
        else:
            messagebox.showwarning("Warning", "No cropped image to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropperApp(root)
    root.mainloop()
