import os
import sys
import customtkinter as ctk
from PIL import Image
import ctypes
import 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNT_FILE = os.path.join(BASE_DIR, "launches.txt")

if os.path.exists(COUNT_FILE):
    try:
        with open(COUNT_FILE, "r") as f:
            launches = int(f.read().strip())
    except ValueError:
        launches = 1
else:
    launches = 1

close_sound = "idiot.wav"
sound_launch1 = "idiot.wav"
sound_launch2 = "ikillyou.wav"
image_file = "image.jpg"

if launches == 2:
    target_sound = sound_launch1
elif launches >= 3:
    target_sound = sound_launch2


def play_audio(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        # SND_ASYNC играет звук в фоновом режиме не останавливая код
        winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)


def stop_audio():
    # Остановка проигрывания
    winsound.PlaySound(None, winsound.SND_PURGE)


def force_close():
    stop_audio()
    app.destroy()


def on_close_click():
    play_audio(close_sound)


def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)


def start_game():
    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 250

    canvas = ctk.CTkCanvas(app, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    player = canvas.create_rectangle(50, 50, 80, 80, fill="cyan")
    enemy = canvas.create_rectangle(180, 150, 210, 180, fill="red")

    def check_collision():
        p_coords = canvas.coords(player)
        e_coords = canvas.coords(enemy)
        if not (p_coords[2] < e_coords[0] or p_coords[0] > e_coords[2] or
                p_coords[3] < e_coords[1] or p_coords[1] > e_coords[3]):
            with open(COUNT_FILE, "w") as f:
                f.write("2")
            force_close()

    def move_player(event):
        key = event.keysym.lower()
        dx, dy = 0, 0
        if key == 'w':
            dy = -10
        elif key == 's':
            dy = 10
        elif key == 'a':
            dx = -10
        elif key == 'd':
            dx = 10

        p_coords = canvas.coords(player)

        
        if (p_coords[0] + dx >= 0 and
                p_coords[2] + dx <= CANVAS_WIDTH and
                p_coords[1] + dy >= 0 and
                p_coords[3] + dy <= CANVAS_HEIGHT):
            canvas.move(player, dx, dy)
            check_collision()

    app.bind("<Key>", move_player)


def show_fullscreen_image():
    app.withdraw()
    play_audio(target_sound)

    img_path = os.path.join(BASE_DIR, image_file)
    if os.path.exists(img_path):
        set_wallpaper(img_path)

        top = ctk.CTkToplevel(app)
        top.overrideredirect(True)
        top.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}+0+0")
        top.attributes("-topmost", True)
        top.protocol("WM_DELETE_WINDOW", lambda: None)

        pil_img = Image.open(img_path)
        screen_w = app.winfo_screenwidth()
        screen_h = app.winfo_screenheight()

        ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(screen_w, screen_h))
        img_label = ctk.CTkLabel(top, image=ctk_img, text="")
        img_label.pack(fill="both", expand=True)

        top.after(10000, force_close)

    with open(COUNT_FILE, "w") as f:
        f.write("1")



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title(" ")
app.geometry("300x250")
app.protocol("WM_DELETE_WINDOW", on_close_click)

if launches == 1:
    start_game()
elif launches == 2:
    with open(COUNT_FILE, "w") as f:
        f.write("3")

    play_audio(target_sound)
    app.after(5000, force_close)
else:
    app.after(100, show_fullscreen_image)

app.mainloop()
