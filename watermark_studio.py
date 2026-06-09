import os
import threading
import json
import urllib.request
import webbrowser
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image

class WatermarkApp:
    CURRENT_VERSION = "2.0"
    # Replace this URL with the raw link to your version.json file online
    UPDATE_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/version.json"

    def __init__(self, root):
        self.root = root
        self.root.withdraw() # Hide root during splash screen

        self.folder_path = StringVar()
        self.include_subfolders = BooleanVar()
        self.position = StringVar(value="bottom right")
        self.replace_existing = BooleanVar()
        self.output_path = StringVar()

        self.watermark_folder = os.path.join(os.getcwd(), "watermarks")
        os.makedirs(self.watermark_folder, exist_ok=True)

        self.apply_theme()
        self.show_splash()

    # ---------------- Application Setup & Styling ----------------
    def apply_theme(self):
        self.is_dark = False
        try:
            import sv_ttk
            import darkdetect
            self.is_dark = darkdetect.theme() == "Dark"
            sv_ttk.set_theme("dark" if self.is_dark else "light")
            
            if not self.is_dark:
                self.root.configure(bg="#ffffff")
                style = ttk.Style()
                style.configure("TFrame", background="#ffffff")
                style.configure("TLabel", background="#ffffff")
                style.configure("TCheckbutton", background="#ffffff")
        except ImportError:
            style = ttk.Style()
            if "clam" in style.theme_names():
                style.theme_use("clam")

    def show_splash(self):
        splash = Toplevel(self.root)
        splash.overrideredirect(True)
        splash.geometry("420x220")
        
        sw = splash.winfo_screenwidth()
        sh = splash.winfo_screenheight()
        splash.geometry(f"+{(sw-420)//2}+{(sh-220)//2}")
        
        f = ttk.Frame(splash)
        f.pack(fill=BOTH, expand=True)
        
        ttk.Label(f, text="💧", font=("Segoe UI", 40)).pack(pady=(30, 5))
        ttk.Label(f, text="Watermark Studio PRO", font=("Segoe UI", 16, "bold")).pack()
        ttk.Label(f, text="Loading components...", font=("Segoe UI", 9)).pack(pady=(15, 0))
        
        splash.update()
        self.root.after(2000, lambda: self.finish_splash(splash))

    def finish_splash(self, splash):
        splash.destroy()
        self.root.title("Watermark Studio PRO")
        self.root.geometry("570x640")
        self.root.resizable(False, False)
        
        # Set Application Logo
        try:
            self.root.iconbitmap("logo.ico")
        except Exception:
            pass

        # Center Main Window
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw-570)//2}+{(sh-640)//2}")
        
        self.build_ui()
        self.build_menu()
        
        # Apply Windows 11 Titlebar Dark Mode
        try:
            import ctypes
            self.root.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            value = ctypes.c_int(2 if self.is_dark else 0)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.root.deiconify()

    def build_menu(self):
        menubar = Menu(self.root)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="Check for Updates", command=self.check_updates)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def check_updates(self):
        # Run the network request in a background thread so the UI doesn't freeze
        threading.Thread(target=self._perform_update_check, daemon=True).start()

    def _perform_update_check(self):
        try:
            # Fetch the version.json file from the internet
            req = urllib.request.Request(self.UPDATE_URL, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("version")
                download_url = data.get("url")

            # Compare online version with the local version
            if latest_version and latest_version != self.CURRENT_VERSION:
                self.root.after(0, lambda: self.prompt_update(latest_version, download_url))
            else:
                self.root.after(0, lambda: messagebox.showinfo("Update Check", "You are currently running the latest version!"))
        except Exception:
            self.root.after(0, lambda: messagebox.showerror("Update Error", "Failed to connect to the update server.\nPlease check your internet connection and try again."))

    def prompt_update(self, latest_version, download_url):
        ans = messagebox.askyesno("Update Available", f"A new version ({latest_version}) is available!\n\nWould you like to download it now?")
        if ans and download_url:
            webbrowser.open(download_url)

    def show_about(self):
        about_win = Toplevel(self.root)
        about_win.title("About Watermark Studio PRO")
        about_win.geometry("320x160")
        about_win.resizable(False, False)
        
        sw = about_win.winfo_screenwidth()
        sh = about_win.winfo_screenheight()
        about_win.geometry(f"+{(sw-320)//2}+{(sh-160)//2}")
        
        f = ttk.Frame(about_win)
        f.pack(fill=BOTH, expand=True)

        ttk.Label(f, text="💧 Watermark Studio PRO", font=("Segoe UI", 12, "bold")).pack(pady=(20, 5))
        ttk.Label(f, text=f"Version {self.CURRENT_VERSION} (Windows 11 Edition)").pack()
        ttk.Label(f, text="© 2026 AI Technology Inc.").pack(pady=(2, 10))
        ttk.Button(f, text="Close", command=about_win.destroy, width=15).pack()

    # ---------------- Build Interface ----------------
    def build_ui(self):
        # Master Background Frame to unify the form and control backgrounds
        bg_frame = ttk.Frame(self.root)
        bg_frame.pack(fill=BOTH, expand=True)

        # Header Banner
        banner_bg = "#0078D4" # Windows Accent Blue
        banner_fg = "#ffffff"
        
        header_frame = Frame(bg_frame, bg=banner_bg)
        header_frame.pack(fill=X)
        
        Label(header_frame, text="💧 Watermark Studio PRO", font=("Segoe UI Variable Display", 22, "bold"), bg=banner_bg, fg=banner_fg).pack(pady=(20, 2))
        Label(header_frame, text="Batch image watermarking made easy", font=("Segoe UI Variable Text", 11), bg=banner_bg, fg=banner_fg).pack(pady=(0, 20))

        # Main Content Frame
        main_frame = ttk.Frame(bg_frame, padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        # --- Input Section ---
        input_lf = ttk.Frame(main_frame)
        input_lf.pack(fill=X, pady=(0, 10))
        
        ttk.Label(input_lf, text="1. Input Settings", font=("Segoe UI Variable Text", 11, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Label(input_lf, text="Image Folder:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(input_lf, textvariable=self.folder_path, width=45).grid(row=1, column=1, padx=15, pady=5)
        ttk.Button(input_lf, text="Browse", command=self.browse_folder).grid(row=1, column=2, pady=5)

        ttk.Checkbutton(input_lf, text="Include subfolders", variable=self.include_subfolders, style="Switch.TCheckbutton").grid(row=2, column=1, sticky="w", pady=(5,0))

        ttk.Separator(main_frame, orient="horizontal").pack(fill=X, pady=(5, 15))

        # --- Watermark Section ---
        wm_lf = ttk.Frame(main_frame)
        wm_lf.pack(fill=X, pady=(0, 10))
        
        ttk.Label(wm_lf, text="2. Watermark Settings", font=("Segoe UI Variable Text", 11, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Label(wm_lf, text="Select Watermark:").grid(row=1, column=0, sticky="w", pady=5)
        self.watermark_combo = ttk.Combobox(wm_lf, width=43, state="readonly")
        self.refresh_watermark_list()
        self.watermark_combo.grid(row=1, column=1, padx=15, pady=5)
        ttk.Button(wm_lf, text="Add New", command=self.add_watermark_image).grid(row=1, column=2, pady=5)

        ttk.Label(wm_lf, text="Position:").grid(row=2, column=0, sticky="w", pady=5)
        pos_combo = ttk.Combobox(wm_lf, width=43, state="readonly", textvariable=self.position)
        pos_combo["values"] = ("top left", "top right", "bottom left", "bottom right")
        pos_combo.grid(row=2, column=1, padx=15, sticky="w", pady=5)
        pos_combo.current(3)

        ttk.Separator(main_frame, orient="horizontal").pack(fill=X, pady=(5, 15))

        # --- Output Section ---
        out_lf = ttk.Frame(main_frame)
        out_lf.pack(fill=X, pady=(0, 10))
        
        ttk.Label(out_lf, text="3. Output Settings", font=("Segoe UI Variable Text", 11, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        ttk.Label(out_lf, text="Output Folder:").grid(row=1, column=0, sticky="w", pady=5)
        self.output_entry = ttk.Entry(out_lf, textvariable=self.output_path, width=45)
        self.output_entry.grid(row=1, column=1, padx=15, pady=5)
        self.output_browse = ttk.Button(out_lf, text="Browse", command=self.browse_output)
        self.output_browse.grid(row=1, column=2, pady=5)

        ttk.Checkbutton(out_lf, text="Replace original images", variable=self.replace_existing, command=self.toggle_output_state, style="Switch.TCheckbutton").grid(row=2, column=1, sticky="w", pady=(5, 0))

        ttk.Separator(main_frame, orient="horizontal").pack(fill=X, pady=(10, 15))

        # --- Bottom Action Area ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(0, 5))

        self.start_btn = Button(action_frame, text="Start Watermarking", command=self.start_thread,
                                bg="#107C10", fg="white", activebackground="#0B5A0B", activeforeground="white",
                                font=("Segoe UI Variable Text", 11, "bold"), relief=FLAT, cursor="hand2")
        self.start_btn.pack(fill=X, ipady=8)

        # Dedicated container to allow safe hiding/showing of progress components
        self.progress_container = ttk.Frame(action_frame)
        self.progress_container.pack(fill=X, pady=(15, 0))

        self.status_label = ttk.Label(self.progress_container, font=("Segoe UI Variable Text", 9))
        self.progress = ttk.Progressbar(self.progress_container, mode="determinate")

    # ---------------- Helpers ----------------
    def show_progress_ui(self, total):
        self.status_label.pack(anchor="w", pady=(0, 5))
        self.progress.pack(fill=X, pady=(0, 5))
        self.status_label.configure(text=f"Starting... 0 of {total}")
        self.progress["maximum"] = total
        self.start_btn.configure(state=DISABLED, bg="#e0e0e0", fg="#888888", cursor="arrow") # Prevent double-clicks

    def update_progress(self, current, total, pct):
        self.progress.configure(value=current)
        self.status_label.configure(text=f"Processing images... {current} of {total} ({pct}%)")

    def finish_processing(self, count):
        self.progress.configure(value=0)
        self.status_label.pack_forget()
        self.progress.pack_forget()
        self.start_btn.configure(state=NORMAL, bg="#107C10", fg="white", cursor="hand2")
        messagebox.showinfo("Done", f"Successfully processed {count} images!")

    def toggle_output_state(self):
        state = "disabled" if self.replace_existing.get() else "normal"
        self.output_entry.configure(state=state)
        self.output_browse.configure(state=state)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def add_watermark_image(self):
        file = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file:
            dest = os.path.join(self.watermark_folder,
                                os.path.basename(file))
            Image.open(file).save(dest)
            self.refresh_watermark_list()
            messagebox.showinfo("Success", "Watermark Added!")

    def refresh_watermark_list(self):
        files = [f for f in os.listdir(self.watermark_folder)
                 if f.lower().endswith(
                     (".png", ".jpg", ".jpeg"))]
        self.watermark_combo["values"] = files
        if files:
            self.watermark_combo.current(0)

    def validate_fields(self):
        if not self.folder_path.get():
            messagebox.showwarning("Error", "Select Image Folder")
            return False
        if not self.watermark_combo.get():
            messagebox.showwarning("Error", "Select Watermark")
            return False
        if not self.replace_existing.get() and not self.output_path.get():
            messagebox.showwarning("Error", "Select Output Folder")
            return False
        return True

    # ---------------- Threading ----------------
    def start_thread(self):
        if not self.validate_fields():
            return
        threading.Thread(
            target=self.process_images,
            daemon=True).start()

    # ---------------- Bulk Processing ----------------
    def process_images(self):
        folder = self.folder_path.get()
        wm_path = os.path.join(
            self.watermark_folder,
            self.watermark_combo.get())

        out_folder = folder if self.replace_existing.get() \
            else self.output_path.get()

        images = []
        for root_dir, _, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(
                        (".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root_dir, f))
            if not self.include_subfolders.get():
                break

        total = len(images)
        if total == 0:
            self.root.after(0, lambda: messagebox.showinfo("Info", "No Images Found"))
            return

        watermark = Image.open(wm_path).convert("RGBA")

        count = 0
        
        self.root.after(0, lambda t=total: self.show_progress_ui(t))

        for img_path in images:
            try:
                with Image.open(img_path).convert("RGBA") as img:

                    wm_w = int(img.width * 0.2)
                    ratio = wm_w / watermark.width
                    wm_h = int(watermark.height * ratio)

                    wm = watermark.resize(
                        (wm_w, wm_h), Image.LANCZOS)

                    layer = Image.new(
                        "RGBA", img.size, (0, 0, 0, 0))

                    pos = {
                        "top left": (10, 10),
                        "top right": (img.width - wm.width - 10, 10),
                        "bottom left": (10, img.height - wm.height - 10),
                        "bottom right": (
                            img.width - wm.width - 10,
                            img.height - wm.height - 10)
                    }[self.position.get()]

                    layer.paste(wm, pos, wm)
                    final = Image.alpha_composite(img, layer)

                    if self.replace_existing.get():
                        out_file = img_path
                    else:
                        rel_path = os.path.relpath(img_path, folder)
                        out_file = os.path.join(out_folder, rel_path)
                        os.makedirs(os.path.dirname(out_file), exist_ok=True)

                    if out_file.lower().endswith(".png"):
                        final.save(out_file, optimize=True)
                    else:
                        final.convert("RGB").save(
                            out_file,
                            "JPEG",
                            quality=85,
                            optimize=True)

                    count += 1
                    pct = int((count / total) * 100)
                    self.root.after(0, lambda c=count, t=total, p=pct: self.update_progress(c, t, p))

            except Exception as e:
                print("Skipped:", img_path, e)

        self.root.after(0, lambda c=count: self.finish_processing(c))


if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)
    root.mainloop()