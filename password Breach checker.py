import customtkinter as ctk
import threading
import hashlib
import requests
import time
import re
from PIL import Image, ImageSequence
from customtkinter import CTkImage

# -------- Password Breach Checking --------
def check_password(pwd):
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1pwd[:5], sha1pwd[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        if response.status_code != 200:
            return False
        hashes = (line.split(':') for line in response.text.splitlines())
        return any(h.startswith(suffix) for h, _ in hashes)
    except Exception:
        return False

# -------- Password Strength Evaluation --------
def evaluate_strength(pwd):
    score = 0
    if len(pwd) >= 8: score += 1
    if re.search(r"[A-Z]", pwd): score += 1
    if re.search(r"[a-z]", pwd): score += 1
    if re.search(r"\d", pwd): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd): score += 1
    strength = (score / 5) * 100
    if strength <= 40:
        return strength, "Weak password", "red"
    elif strength <= 70:
        return strength, "Moderate password", "orange"
    else:
        return strength, "Strong paasword", "green"

# -------- Spinner Animation Using GIF --------
def animate_gif():
    loader_label.configure(image=frames[0])
    frame_index = 0
    while loader_visible:
        loader_label.configure(image=frames[frame_index % len(frames)])
        frame_index += 1
        time.sleep(0.1)
    loader_label.configure(image=None)

# -------- Main Password Check Thread --------
def run_check():
    global loader_visible
    password = entry.get()
    if not password:
        result_label.configure(text="Please enter a password", text_color="orange")
        return

    result_label.configure(text="")
    loader_visible = True
    threading.Thread(target=animate_gif).start()

    breached = check_password(password)
    loader_visible = False
    time.sleep(0.1)

    if breached:
        result_label.configure(text="❌ Breached Password!", text_color="red")
    else:
        result_label.configure(text="✅ Safe Password", text_color="green")

def threaded_check():
    threading.Thread(target=run_check).start()

# -------- Live Password Strength Update --------
def update_strength_bar(*args):
    pwd = entry.get()
    strength, label, color = evaluate_strength(pwd)
    strength_bar.set(strength / 100)
    strength_label.configure(text=f"Strength: {label}", text_color=color)
    strength_bar.configure(progress_color=color)

# -------- Light/Dark Mode Switch --------
def toggle_mode():
    if theme_switch.get() == 1:
        ctk.set_appearance_mode("light")
        theme_switch.configure(text="Dark Mode")
    else:
        ctk.set_appearance_mode("dark")
        theme_switch.configure(text="Light Mode")

# -------- Password Visibility Toggle --------
is_password_hidden = True
def toggle_password_visibility():
    global is_password_hidden
    is_password_hidden = not is_password_hidden
    entry.configure(show="*" if is_password_hidden else "")
    eye_button.configure(text="👁️" if is_password_hidden else "🙈")

# -------- GUI Setup --------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("🔐 Password Breach Checker")
app.geometry("500x430")
app.iconbitmap("viking.ico")  # or use wm_iconphoto for PNG

title = ctk.CTkLabel(app, text="Enter a password to check:", font=ctk.CTkFont(size=18, weight="bold"))
title.pack(pady=(30, 10))

# Entry frame with toggle button
entry_frame = ctk.CTkFrame(app, fg_color="transparent")
entry_frame.pack(pady=10)

entry = ctk.CTkEntry(entry_frame, placeholder_text="Your password", show="*", width=250)
entry.pack(side="left", padx=(0, 5))
entry.bind("<KeyRelease>", update_strength_bar)

eye_button = ctk.CTkButton(entry_frame, text="👁️", width=40, command=toggle_password_visibility)
eye_button.pack(side="left")

strength_bar = ctk.CTkProgressBar(app, width=300)
strength_bar.pack(pady=(5, 2))
strength_bar.set(0)

strength_label = ctk.CTkLabel(app, text="Strength: ", font=ctk.CTkFont(size=14))
strength_label.pack()

check_btn = ctk.CTkButton(app, text="Check Password", command=threaded_check)
check_btn.pack(pady=15)

result_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=16))
result_label.pack(pady=5)

# -------- Loader GIF Setup --------
loader_visible = False
loader_label = ctk.CTkLabel(app, text="")
loader_label.pack(pady=(10, 10))

gif = Image.open("Ghost.gif")
frames = [CTkImage(light_image=frame.copy().convert("RGBA"), size=(64, 64))
          for frame in ImageSequence.Iterator(gif)]

# -------- Theme Toggle --------
initial_mode = ctk.get_appearance_mode()
theme_switch = ctk.CTkSwitch(app, text="Dark Mode" if initial_mode == "light" else "Light Mode", command=toggle_mode)
theme_switch.pack(pady=5)
theme_switch.select() if initial_mode == "light" else theme_switch.deselect()

app.mainloop()
