import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

# --- Import the C++ module ---
# This will fail if you haven't compiled the C++ code yet.
# The compiled file will be named something like 'VisionCraft_cpp.cpython-310-x86_64-linux-gnu.so'
try:
    import visioncraft_cpp
except ImportError:
    print("ERROR: Could not import the C++ module 'VisionCraft_cpp'.")
    print("Please make sure you have compiled the C++ code using CMake.")
    exit()
# -----------------------------


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VisionCraft")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2E2E2E")

        self.original_image = None
        self.processed_image = None
        self.image_path = None
        self.display_image_tk = None

        # --- For cropping ---
        self.crop_rect = None
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.is_drawing = False
        
        # --- For Undo Functionality ---
        self.history = []

        # --- Layout Frames ---
        control_frame = tk.Frame(root, bg="#3C3C3C", padx=10, pady=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.image_frame = tk.Frame(root, bg="#2E2E2E", padx=10, pady=10)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Controls ---
        tk.Label(control_frame, text="VisionCraft Controls", font=("Helvetica", 16, "bold"), fg="white", bg="#3C3C3C").pack(pady=10)

        self.load_button = tk.Button(control_frame, text="Load Image", command=self.load_image, bg="#555", fg="white", relief="flat", width=20)
        self.load_button.pack(pady=5)
        
        self.crop_button = tk.Button(control_frame, text="Crop to Selection", command=self.perform_crop, bg="#F39C12", fg="white", relief="flat", width=20, state=tk.DISABLED)
        self.crop_button.pack(pady=(20, 5))

        # --- Rotate Buttons ---
        rotate_frame = tk.Frame(control_frame, bg="#3C3C3C")
        rotate_frame.pack(pady=5)
        self.rotate_left_button = tk.Button(rotate_frame, text="Rotate Left", command=lambda: self.apply_rotation(-90), bg="#555", fg="white", relief="flat", width=9, state=tk.DISABLED)
        self.rotate_left_button.pack(side=tk.LEFT, padx=(0, 2))
        self.rotate_right_button = tk.Button(rotate_frame, text="Rotate Right", command=lambda: self.apply_rotation(90), bg="#555", fg="white", relief="flat", width=9, state=tk.DISABLED)
        self.rotate_right_button.pack(side=tk.RIGHT, padx=(2, 0))


        tk.Label(control_frame, text="Filters", font=("Helvetica", 14), fg="white", bg="#3C3C3C").pack(pady=(10, 5))

        self.filter_buttons = {
            "Grayscale": tk.Button(control_frame, text="Grayscale", command=lambda: self.apply_filter("grayscale"), bg="#555", fg="white", relief="flat", width=20),
            "Blur": tk.Button(control_frame, text="Blur", command=lambda: self.apply_filter("blur"), bg="#555", fg="white", relief="flat", width=20),
            "Edges": tk.Button(control_frame, text="Edge Detection", command=lambda: self.apply_filter("edges"), bg="#555", fg="white", relief="flat", width=20),
            "Sharpen": tk.Button(control_frame, text="Sharpen", command=lambda: self.apply_filter("sharpen"), bg="#555", fg="white", relief="flat", width=20),
        }

        for btn in self.filter_buttons.values():
            btn.pack(pady=5)
            btn.config(state=tk.DISABLED)

        self.reset_button = tk.Button(control_frame, text="Reset Image", command=self.reset_image, bg="#C0392B", fg="white", relief="flat", width=20, state=tk.DISABLED)
        self.reset_button.pack(pady=(20, 5))

        self.save_button = tk.Button(control_frame, text="Save Image", command=self.save_image, bg="#27AE60", fg="white", relief="flat", width=20, state=tk.DISABLED)
        self.save_button.pack(pady=5)

        # --- Undo Button ---
        self.undo_button = tk.Button(control_frame, text="Undo", command=self.undo_last_action, bg="#8E44AD", fg="white", relief="flat", width=20, state=tk.DISABLED)
        self.undo_button.pack(pady=5)

        # --- Image Display ---
        self.canvas = tk.Canvas(self.image_frame, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_text(500, 350, text="Load an image to begin", font=("Helvetica", 20), fill="gray", anchor="center")

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if not self.image_path: return

        self.original_image = cv2.imread(self.image_path)
        if self.original_image is None:
            messagebox.showerror("Error", "Failed to load image.")
            return

        self.reset_image()
        
        for btn in self.filter_buttons.values(): btn.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.rotate_left_button.config(state=tk.NORMAL)
        self.rotate_right_button.config(state=tk.NORMAL)


    def display_image(self, image_cv):
        self.canvas.delete("all")
        
        if len(image_cv.shape) == 2:
            image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        
        image_pil = Image.fromarray(image_rgb)
        
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2:
            self.root.after(50, lambda: self.display_image(image_cv))
            return
            
        img_w, img_h = image_pil.size
        self.display_ratio = min(canvas_w / img_w, canvas_h / img_h)
        self.display_size = (int(img_w * self.display_ratio), int(img_h * self.display_ratio))
        
        if self.display_size[0] > 0 and self.display_size[1] > 0:
            image_pil = image_pil.resize(self.display_size, Image.Resampling.LANCZOS)

        self.display_image_tk = ImageTk.PhotoImage(image_pil)
        
        self.img_canvas_x = (canvas_w - self.display_size[0]) // 2
        self.img_canvas_y = (canvas_h - self.display_size[1]) // 2
        
        self.canvas.create_image(self.img_canvas_x, self.img_canvas_y, anchor=tk.NW, image=self.display_image_tk)

    def save_state_for_undo(self):
        """Saves the current state of the processed image for the undo stack."""
        if self.processed_image is not None:
            self.history.append(self.processed_image.copy())
            self.undo_button.config(state=tk.NORMAL)

    def undo_last_action(self):
        """Reverts the image to its previous state from the history."""
        if self.history:
            self.processed_image = self.history.pop()
            self.display_image(self.processed_image)
        
        if not self.history:
            self.undo_button.config(state=tk.DISABLED)

    def apply_filter(self, filter_name):
        if self.processed_image is None: return
        self.save_state_for_undo()

        if len(self.processed_image.shape) == 2:
            self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2BGR)

        if filter_name == "grayscale": self.processed_image = visioncraft_cpp.to_grayscale(self.processed_image)
        elif filter_name == "blur": self.processed_image = visioncraft_cpp.apply_blur(self.processed_image)
        elif filter_name == "edges": self.processed_image = visioncraft_cpp.detect_edges(self.processed_image)
        elif filter_name == "sharpen": self.processed_image = visioncraft_cpp.sharpen_image(self.processed_image)
        
        self.display_image(self.processed_image)

    def apply_rotation(self, angle):
        if self.processed_image is None: return
        self.save_state_for_undo()
        self.processed_image = visioncraft_cpp.rotate_image(self.processed_image, angle)
        self.display_image(self.processed_image)

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image)
            self.crop_button.config(state=tk.DISABLED)
            self.history.clear()
            self.undo_button.config(state=tk.DISABLED)

    def save_image(self):
        if self.processed_image is None: return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if save_path:
            cv2.imwrite(save_path, self.processed_image)
            messagebox.showinfo("Success", f"Image saved to {save_path}")

    def on_mouse_press(self, event):
        self.is_drawing = True
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        if self.crop_rect:
            self.canvas.delete(self.crop_rect)
        self.crop_rect = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_start_x, self.crop_start_y, outline='red', width=2)
        self.crop_button.config(state=tk.DISABLED)

    def on_mouse_drag(self, event):
        if not self.is_drawing: return
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        self.canvas.coords(self.crop_rect, self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y)

    def on_mouse_release(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.crop_button.config(state=tk.NORMAL)

    def perform_crop(self):
        if self.processed_image is None or not self.crop_rect: return

        img_x_start_on_canvas = self.img_canvas_x
        img_y_start_on_canvas = self.img_canvas_y
        img_x_end_on_canvas = self.img_canvas_x + self.display_size[0]
        img_y_end_on_canvas = self.img_canvas_y + self.display_size[1]

        clamped_x1 = max(img_x_start_on_canvas, min(self.crop_start_x, img_x_end_on_canvas))
        clamped_y1 = max(img_y_start_on_canvas, min(self.crop_start_y, img_y_end_on_canvas))
        clamped_x2 = max(img_x_start_on_canvas, min(self.crop_end_x, img_x_end_on_canvas))
        clamped_y2 = max(img_y_start_on_canvas, min(self.crop_end_y, img_y_end_on_canvas))

        x1 = int((clamped_x1 - self.img_canvas_x) / self.display_ratio)
        y1 = int((clamped_y1 - self.img_canvas_y) / self.display_ratio)
        x2 = int((clamped_x2 - self.img_canvas_x) / self.display_ratio)
        y2 = int((clamped_y2 - self.img_canvas_y) / self.display_ratio)

        crop_x = min(x1, x2)
        crop_y = min(y1, y2)
        crop_w = abs(x2 - x1)
        crop_h = abs(y2 - y1)
        
        if crop_w > 0 and crop_h > 0:
            self.save_state_for_undo()
            self.processed_image = visioncraft_cpp.crop_image(self.processed_image, crop_x, crop_y, crop_w, crop_h)
            self.display_image(self.processed_image)
        
        self.canvas.delete(self.crop_rect)
        self.crop_rect = None
        self.crop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()