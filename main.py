"""
HIT137 Assignment 3 - Tkinter AI GUI Application
Demonstrates all required OOP concepts:
1. Multiple Inheritance
2. Multiple Decorators
3. Encapsulation
4. Polymorphism
5. Method Overriding
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import threading
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.text_to_video import TextToVideoModel
from models.image_classifier import ImageClassifierModel
from utils.decorators import log_execution, timer, error_handler
from gui.base_window import GUIBase, LabelFrameBase


# Dark Theme Color Scheme 
class DarkTheme:
    """Dark theme color palette inspired by CustomTkinter"""
    PRIMARY = "#1f6aa5"
    SECONDARY = "#144870"
    SUCCESS = "#2fa572"
    WARNING = "#f59e0b"
    BG_DARK = "#1a1a1a"
    BG_CARD = "#2b2b2b"
    BG_HOVER = "#3a3a3a"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    BORDER = "#404040"
    HOVER = "#2a8fd5"


# Rounded Button Widget 
class RoundedButton(tk.Canvas):
    """Custom rounded button matching mockup design with blue outline"""

    def __init__(self, parent, text="Button", command=None, bg_color=None,
                 fg_color="white", border_color=None, width=140, height=35):
        super().__init__(parent, width=width, height=height,
                        bg=bg_color or DarkTheme.BG_CARD,
                        highlightthickness=0)

        self.command = command
        self.bg_color = bg_color or DarkTheme.BG_CARD
        self.border_color = border_color or DarkTheme.PRIMARY
        self.fg_color = fg_color
        self.text = text
        self.radius = 8

        self._draw_button()
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _draw_button(self, hover=False):
        self.delete("all")
        fill_color = DarkTheme.BG_HOVER if hover else self.bg_color

        # Draw rounded rectangle with border
        self.create_rounded_rect(2, 2, self.winfo_reqwidth()-2,
                                 self.winfo_reqheight()-2,
                                 self.radius, fill_color, self.border_color)

        # Draw text
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=self.text, fill=self.fg_color,
                        font=("Segoe UI", 10))

    def create_rounded_rect(self, x1, y1, x2, y2, radius, fill, outline):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, fill=fill,
                                   outline=outline, width=2)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        self._draw_button(hover=True)

    def _on_leave(self, event):
        self._draw_button(hover=False)


# Rounded Frame Widget for cards
class RoundedFrame(tk.Canvas):
    """Custom rounded frame for card-like containers"""

    def __init__(self, parent, bg_color=None, border_color=None, radius=10, **kwargs):
        super().__init__(parent, bg=DarkTheme.BG_DARK,
                        highlightthickness=0, **kwargs)

        self.bg_color = bg_color or DarkTheme.BG_CARD
        self.border_color = border_color or DarkTheme.BORDER
        self.radius = radius

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.delete("all")
        w, h = event.width, event.height
        r = self.radius

        # Create rounded rectangle
        points = [
            r, 0,
            w-r, 0,
            w, 0,
            w, r,
            w, h-r,
            w, h,
            w-r, h,
            r, h,
            0, h,
            0, h-r,
            0, r,
            0, 0
        ]
        self.create_polygon(points, smooth=True,
                           fill=self.bg_color,
                           outline=self.border_color, width=1)


# Mixin class for multiple inheritance
class ModelManagerMixin:
    """
    Mixin class for managing AI models
    Demonstrates Multiple Inheritance when combined with GUI classes
    """

    def init_models(self):
        """Initialize AI models"""
        self.text_to_video_model = TextToVideoModel()
        self.image_model = ImageClassifierModel()
        self.current_model = None
        self.models_loaded = {"text_to_video": False, "image": False}

    @timer
    @log_execution
    def load_model_async(self, model_type):
        """Load model in separate thread"""
        success = False
        if model_type == "text_to_video":
            success = self.text_to_video_model.load_model()
            self.models_loaded["text_to_video"] = success
        elif model_type == "image":
            success = self.image_model.load_model()
            self.models_loaded["image"] = success
        return success


# Multiple Inheritance: Inherits from both tk.Tk and ModelManagerMixin
class AIGUIApplication(tk.Tk, ModelManagerMixin):
    """
    Main Application Class
    Demonstrates MULTIPLE INHERITANCE from tk.Tk and ModelManagerMixin
    """

    def __init__(self):
        tk.Tk.__init__(self)
        ModelManagerMixin.init_models(self)

        self._window_title = "AI Studio - HIT137"
        self._window_geometry = "1200x800"
        self._selected_model = tk.StringVar(value="Text-to-Video")
        self._input_type = tk.StringVar(value="Text")
        self._selected_image_path = None
        self._generated_image = None

        self._setup_window()
        self._setup_styles()
        self._create_widgets()

    def _setup_window(self):
        """Private method - demonstrates encapsulation"""
        self.title(self._window_title)
        self.geometry(self._window_geometry)
        self.configure(bg=DarkTheme.BG_DARK)

        # Apply rounded corners on Windows 11
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            DWMWCP_ROUND = 2
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(ctypes.c_int(DWMWCP_ROUND)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            pass  # Silently fail if not on Windows 11

    def _setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TCombobox',
                       fieldbackground=DarkTheme.BG_CARD,
                       background=DarkTheme.PRIMARY,
                       foreground=DarkTheme.TEXT_PRIMARY)

        # Progress bar style
        style.configure('TProgressbar',
                       background=DarkTheme.PRIMARY,
                       troughcolor=DarkTheme.BG_HOVER,
                       bordercolor=DarkTheme.BORDER,
                       lightcolor=DarkTheme.PRIMARY,
                       darkcolor=DarkTheme.PRIMARY)

    def _create_widgets(self):
        """Create all GUI widgets"""
        self._create_menu()
        self._create_header()

        main_container = tk.Frame(self, bg=DarkTheme.BG_DARK)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        self._create_user_input_section(main_container)
        self._create_output_section(main_container)
        self._create_info_section()

    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self, bg="#1e293b", fg="white")
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Load Text-to-Image", command=lambda: self._load_specific_model("text_to_image"))
        models_menu.add_command(label="Load Image Classification", command=lambda: self._load_specific_model("image"))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

    def _create_header(self):
        """Create header"""
        header = tk.Frame(self, bg=DarkTheme.PRIMARY, height=100)
        header.pack(fill="x")

        tk.Label(header, text="AI Studio", font=("Segoe UI", 24, "bold"),
                bg=DarkTheme.PRIMARY, fg="white").pack(side="left", padx=30, pady=20)

        tk.Label(header, text="Text-to-Video & Image Classification",
                font=("Segoe UI", 11), bg=DarkTheme.PRIMARY,
                fg="#bfdbfe").pack(side="left")

        selection_frame = tk.Frame(header, bg=DarkTheme.PRIMARY)
        selection_frame.pack(side="right", padx=30)

        tk.Label(selection_frame, text="Select Model:", font=("Segoe UI", 10),
                bg=DarkTheme.PRIMARY, fg="white").pack(side="left", padx=10)

        ttk.Combobox(selection_frame, textvariable=self._selected_model,
                    values=["Text-to-Video", "Image Classification"],
                    state="readonly", width=22, style='Modern.TCombobox').pack(side="left")

        RoundedButton(selection_frame, text="Load Model",
                     command=self._load_selected_model,
                     border_color=DarkTheme.SUCCESS,
                     width=120, height=35).pack(side="left", padx=10)

    def _create_card(self, parent, title):
        """Create a modern card container with better styling"""
        card = tk.Frame(parent, bg=DarkTheme.BG_CARD,
                       highlightbackground=DarkTheme.BORDER,
                       highlightthickness=1)

        # Title with better typography
        title_label = tk.Label(card, text=title,
                              font=("Segoe UI", 13, "bold"),
                              bg=DarkTheme.BG_CARD,
                              fg=DarkTheme.TEXT_PRIMARY)
        title_label.pack(anchor="w", padx=20, pady=(15, 10))

        # Subtle separator line
        tk.Frame(card, bg=DarkTheme.BORDER, height=1).pack(fill="x", padx=20, pady=(0, 10))
        return card

    def _create_user_input_section(self, parent):
        """Create input section"""
        card = self._create_card(parent, "User Input")
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        content = tk.Frame(card, bg=DarkTheme.BG_CARD)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Text input section
        tk.Label(content, text="Enter Text Prompt for Video:",
                font=("Segoe UI", 10, "bold"),
                bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))

        self.text_input = scrolledtext.ScrolledText(content, height=4, width=40,
                                                   font=("Segoe UI", 10), relief="flat",
                                                   bg=DarkTheme.BG_HOVER, fg=DarkTheme.TEXT_PRIMARY,
                                                   insertbackground=DarkTheme.TEXT_PRIMARY,
                                                   wrap=tk.WORD)
        self.text_input.pack(fill="x", pady=(0, 15))
        self.text_input.insert("1.0", "A beautiful sunset over the ocean with waves")

        # Image input section for Model 2
        tk.Label(content, text="Or Select Input Image (for Model 2):",
                font=("Segoe UI", 10, "bold"),
                bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY).pack(anchor="w", pady=(15, 10))

        RoundedButton(content, text="Browse Image", command=self._browse_image,
                     border_color=DarkTheme.PRIMARY, width=140, height=35).pack(pady=(0, 10))

        self.image_path_label = tk.Label(content, text="", fg=DarkTheme.PRIMARY,
                                        bg=DarkTheme.BG_CARD)
        self.image_path_label.pack()

        btn_frame = tk.Frame(content, bg=DarkTheme.BG_CARD)
        btn_frame.pack(pady=15)

        # Use rounded buttons matching mockup.png style
        RoundedButton(btn_frame, text="Run Model 1",
                     command=lambda: self._run_model(1),
                     border_color=DarkTheme.PRIMARY).pack(side="left", padx=5)

        RoundedButton(btn_frame, text="Run Model 2",
                     command=lambda: self._run_model(2),
                     border_color=DarkTheme.WARNING).pack(side="left", padx=5)

        RoundedButton(btn_frame, text="Clear",
                     command=self._clear_all,
                     border_color=DarkTheme.TEXT_SECONDARY).pack(side="left", padx=5)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    def _create_output_section(self, parent):
        """Create output section"""
        card = self._create_card(parent, "Model Output")
        card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        content = tk.Frame(card, bg=DarkTheme.BG_CARD)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        img_frame = tk.Frame(content, bg="#3a3a3a", highlightbackground=DarkTheme.BORDER, highlightthickness=2)
        img_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.image_display_label = tk.Label(img_frame, text="Video preview will appear here",
                                           bg="#3a3a3a", fg=DarkTheme.TEXT_SECONDARY,
                                           font=("Segoe UI", 11))
        self.image_display_label.pack(expand=True, fill="both")

        # Text output label
        tk.Label(content, text="Text Output:",
                font=("Segoe UI", 10, "bold"),
                bg=DarkTheme.BG_CARD,
                fg=DarkTheme.TEXT_PRIMARY).pack(anchor="w", pady=(0, 8))

        self.output_display = scrolledtext.ScrolledText(content, height=6, width=50,
                                                       font=("Consolas", 9), relief="flat",
                                                       bg=DarkTheme.BG_CARD, fg=DarkTheme.TEXT_PRIMARY,
                                                       insertbackground=DarkTheme.TEXT_PRIMARY,
                                                       wrap=tk.WORD)
        self.output_display.pack(fill="both", pady=(0, 10))

        # Progress bar section
        progress_frame = tk.Frame(content, bg=DarkTheme.BG_CARD)
        progress_frame.pack(fill="x")

        self.progress_label = tk.Label(progress_frame, text="Ready",
                                       font=("Segoe UI", 9),
                                       bg=DarkTheme.BG_CARD,
                                       fg=DarkTheme.TEXT_SECONDARY)
        self.progress_label.pack(anchor="w", pady=(0, 5))

        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                           length=300, maximum=100)
        self.progress_bar.pack(fill="x")

    def _create_info_section(self):
        """Create info section"""
        container = tk.Frame(self, bg=DarkTheme.BG_DARK)
        container.pack(fill="both", padx=20, pady=(0, 20))

        left_card = self._create_card(container, "Model Information")
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_card = self._create_card(container, "OOP Concepts")
        right_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        left_content = tk.Frame(left_card, bg=DarkTheme.BG_CARD)
        left_content.pack(fill="both", expand=True, padx=20, pady=15)

        self.model_info_display = tk.Text(left_content, height=4, font=("Segoe UI", 10),
                                         bg="#2b2b2b", fg=DarkTheme.TEXT_SECONDARY,
                                         relief="flat", padx=15, pady=12,
                                         insertbackground=DarkTheme.TEXT_PRIMARY,
                                         wrap=tk.WORD)
        self.model_info_display.pack(fill="both", expand=True)
        self.model_info_display.insert("1.0", "💡 Select a model to view information...")

        right_content = tk.Frame(right_card, bg=DarkTheme.BG_CARD)
        right_content.pack(fill="both", expand=True, padx=20, pady=15)

        self.oop_info_display = tk.Text(right_content, height=4, font=("Segoe UI", 10),
                                       bg="#2b2b2b", fg=DarkTheme.TEXT_SECONDARY,
                                       relief="flat", padx=15, pady=12,
                                       insertbackground=DarkTheme.TEXT_PRIMARY,
                                       wrap=tk.WORD)
        self.oop_info_display.pack(fill="both", expand=True)

        oop_text = """✓ Multiple Inheritance: Line 174
✓ Encapsulation: Private attributes
✓ Polymorphism: predict() method
✓ Method Overriding: load_model()
✓ Multiple Decorators: @timer @log_execution"""
        self.oop_info_display.insert("1.0", oop_text)

    @error_handler(default_return=None)
    def _toggle_input_type(self):
        """Toggle input type"""
        if self._input_type.get() == "Image":
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", "Select an image using Browse")
            self.text_input.config(state="disabled")
        else:
            self.text_input.config(state="normal")
            self.text_input.delete("1.0", tk.END)

    @error_handler(default_return=None)
    def _browse_image(self):
        """Browse for image"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp"), ("All", "*.*")])
        if file_path:
            self._selected_image_path = file_path
            self.image_path_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self._input_type.set("Image")
            self._toggle_input_type()

    @error_handler(default_return=None)
    def _on_model_change(self, event=None):
        """Handle model change"""
        self._update_model_info(self._selected_model.get())

    def _update_model_info(self, model_name):
        """Update model info"""
        self.model_info_display.config(state="normal")
        self.model_info_display.delete("1.0", tk.END)

        info = self.text_to_video_model.get_model_info() if model_name == "Text-to-Video" else self.image_model.get_model_info()

        info_text = "\n".join([f"• {k}: {v}" for k, v in info.items()])
        self.model_info_display.insert("1.0", info_text)
        self.model_info_display.config(state="disabled")

    def _update_progress(self, percentage, message):
        """Update progress bar and label"""
        self.progress_bar['value'] = percentage
        self.progress_label.config(text=f"{message} ({percentage}%)")

    @timer
    @log_execution
    def _load_selected_model(self):
        """Load model"""
        model_name = self._selected_model.get()
        self.output_display.delete("1.0", tk.END)
        self.output_display.insert("1.0", f"Loading {model_name}...\n")

        # Reset progress
        self.after(0, lambda: self._update_progress(0, "Starting..."))

        def load_thread():
            success = False
            try:
                if model_name == "Text-to-Video":
                    self.after(0, lambda: self._update_progress(20, "Downloading model..."))
                    success = self.load_model_async("text_to_video")
                    self.after(0, lambda: self._update_progress(100, "Model loaded!"))
                    msg = "✅ Text-to-Video loaded successfully!" if success else "❌ Failed to load Text-to-Video"
                else:
                    self.after(0, lambda: self._update_progress(20, "Loading model..."))
                    success = self.load_model_async("image")
                    self.after(0, lambda: self._update_progress(100, "Model loaded!"))
                    msg = "✅ Image Classification loaded successfully!" if success else "❌ Failed to load Image Classification"

                self.after(0, lambda: self.output_display.insert(tk.END, f"\n{msg}\n"))
                self.after(0, lambda: self._update_model_info(model_name))

                # Reset progress after a moment
                self.after(2000, lambda: self._update_progress(0, "Ready"))

            except Exception as e:
                import traceback
                error_msg = str(e) if str(e) else "An unknown error occurred during model loading"
                error_trace = traceback.format_exc()
                print(f"[ERROR in load_thread]: {error_msg}")
                print(f"[TRACEBACK]: {error_trace}")

                detailed_error = f"{error_msg}\n\nDetails: {type(e).__name__}"
                self.after(0, lambda msg=detailed_error: messagebox.showerror("Model Loading Error", msg))
                self.after(0, lambda msg=error_msg: self.output_display.insert(tk.END, f"\n❌ Loading Error: {msg}\n"))
                self.after(0, lambda trace=error_trace: self.output_display.insert(tk.END, f"\nFull error:\n{trace}\n"))
                self.after(0, lambda: self._update_progress(0, "Loading failed"))

        threading.Thread(target=load_thread, daemon=True).start()

    def _load_specific_model(self, model_type):
        """Load specific model"""
        self._selected_model.set("Text-to-Image" if model_type == "text_to_image" else "Image Classification")
        self._load_selected_model()

    def _run_model(self, model_num):
        """Run model - demonstrates polymorphism"""
        model = self.text_to_video_model if model_num == 1 else self.image_model
        model_type = "text_to_video" if model_num == 1 else "image"

        if not self.models_loaded.get(model_type, False):
            messagebox.showwarning("Warning", "Please load the model first!")
            return

        self.output_display.delete("1.0", tk.END)
        self.output_display.insert("1.0", f"Running Model {model_num}...\n\n")

        # Reset progress
        self.after(0, lambda: self._update_progress(0, "Initializing..."))

        def run_thread():
            try:
                if model_type == "text_to_video":
                    # Get text prompt
                    text_prompt = self.text_input.get("1.0", tk.END).strip()
                    if not text_prompt:
                        raise ValueError("Please enter a text prompt for video generation")

                    self.after(0, lambda: self._update_progress(10, "Preparing prompt..."))
                    self.after(0, lambda: self.output_display.insert(tk.END, f"Generating video from: '{text_prompt}'\n\n"))

                    self.after(0, lambda: self._update_progress(20, "Starting video generation..."))
                    self.after(0, lambda: self._update_progress(50, "Generating image from text..."))

                    result = model.predict(text_prompt)

                    self.after(0, lambda: self._update_progress(95, "Exporting video..."))

                    if result is None:
                        raise Exception("Model returned no result. Please check if the model is properly loaded.")

                    output = f"✅ Video Generation Complete!\n\n"
                    output += f"📄 File: {result.get('file', 'N/A')}\n"
                    output += f"🎬 Frames: {result.get('frames', 'N/A')}\n"
                    output += f"⏱️ Duration: {result.get('duration', 'N/A')}\n"
                    output += f"🎞️ FPS: {result.get('fps', 'N/A')}\n"
                    output += f"📦 Format: {result.get('format', 'N/A')}\n"
                    output += f"💬 Status: {result.get('message', 'N/A')}\n"

                    # Display preview image if available
                    if result.get('preview') and os.path.exists(result['preview']):
                        preview_img = Image.open(result['preview'])
                        self.after(0, lambda: self._display_image(preview_img))

                    self.after(0, lambda: self.output_display.insert(tk.END, output))
                    self.after(0, lambda: self._update_progress(100, "Video generation complete!"))
                else:
                    if not self._selected_image_path:
                        raise ValueError("Please select an image")

                    self.after(0, lambda: self._update_progress(20, "Loading image..."))
                    input_img = Image.open(self._selected_image_path)
                    self.after(0, lambda: self._display_image(input_img))

                    self.after(0, lambda: self._update_progress(50, "Classifying image..."))
                    result = model.predict(self._selected_image_path)

                    output = "Classification:\n"
                    for res in result:
                        output += f"  {res['rank']}. {res['label']}: {res['confidence']}\n"

                    self.after(0, lambda: self.output_display.insert(tk.END, output))
                    self.after(0, lambda: self._update_progress(100, "Classification complete!"))

                # Reset progress after a moment
                self.after(3000, lambda: self._update_progress(0, "Ready"))

            except Exception as e:
                import traceback
                error_msg = str(e) if str(e) else "An unknown error occurred"
                error_trace = traceback.format_exc()
                print(f"[ERROR in _run_model]: {error_msg}")
                print(f"[TRACEBACK]: {error_trace}")

                # Show detailed error to user
                detailed_error = f"{error_msg}\n\nDetails: {type(e).__name__}"
                self.after(0, lambda msg=detailed_error: messagebox.showerror("Error", msg))
                self.after(0, lambda msg=error_msg: self.output_display.insert(tk.END, f"\n❌ Error: {msg}\n"))
                self.after(0, lambda trace=error_trace: self.output_display.insert(tk.END, f"\nFull error:\n{trace}\n"))
                self.after(0, lambda: self._update_progress(0, "Error occurred"))

        threading.Thread(target=run_thread, daemon=True).start()

    def _display_image(self, pil_image):
        """Display image"""
        pil_copy = pil_image.copy()
        pil_copy.thumbnail((450, 320), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(pil_copy)
        self.image_display_label.configure(image=photo, text="")
        self.image_display_label.image = photo

    def _clear_all(self):
        """Clear all"""
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", "A beautiful sunset over the ocean with waves")
        self.output_display.delete("1.0", tk.END)
        self._selected_image_path = None
        self._generated_image = None
        self.image_path_label.config(text="")
        self.image_display_label.configure(image="", text="Video preview will appear here")
        self.image_display_label.image = None

    def _show_about(self):
        """Show about"""
        messagebox.showinfo("About", "HIT137 Assignment 3\n\nAI Studio\n\nDemonstrates all OOP concepts")


if __name__ == "__main__":
    print("Starting AI Studio...")
    app = AIGUIApplication()
    app.mainloop()
