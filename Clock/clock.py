import tkinter as tk
import time
import math
from PIL import Image, ImageTk

# 解像度調整
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

SIDE = 500  # ウィンドウの一辺
CENTER = SIDE/2    # ウィンドウの中心

# ウィンドウの作成
root = tk.Tk()
#root.title("Analog Clock")

# キャンバスの作成
canvas = tk.Canvas(root, width = SIDE, height = SIDE)
canvas.pack()

INNER_FRAME_RADIUS = (SIDE * 0.85) / 2 #内枠の半径
CLOCK_FACE_RADIUS = (SIDE * 0.8) / 2 # 時計版の半径

# 外枠を描画
outer_frame = canvas.create_oval(
    3, 3,
    SIDE-3, SIDE-3,
    fill = '#ffffff'
)

# 内枠を描画
inner_frame = canvas.create_oval(
    CENTER - INNER_FRAME_RADIUS, CENTER - INNER_FRAME_RADIUS,
    CENTER + INNER_FRAME_RADIUS, CENTER + INNER_FRAME_RADIUS,
    fill = "#ffffff", outline = '#000000', width = SIDE * 0.01,
)

"""
# 時計盤を描画
clock_face = canvas.create_oval(
    CENTER - CLOCK_FACE_RADIUS, CENTER - CLOCK_FACE_RADIUS,
    CENTER + CLOCK_FACE_RADIUS, CENTER + CLOCK_FACE_RADIUS,
    fill = '#ffffff'
)
"""

# 時針の作成
hour_hand = canvas.create_line(
    CENTER, CENTER, 0, 0,
    fill = '#000000',
    width = CLOCK_FACE_RADIUS * 0.04
)

# 分針の作成
minute_hand = canvas.create_line(
    CENTER, CENTER, 0, 0,
    fill = '#000000',
    width = CLOCK_FACE_RADIUS * 0.02
)

# 秒針の作成
second_hand = canvas.create_line(
    CENTER, CENTER, 0, 0,
    fill = '#000000',
    width = CLOCK_FACE_RADIUS * 0.01
)

animal_images = []
am = ['./mouse.png', './cow.png', './tiger.png', './rabbit.png', './dragon.png', './python.png']
pm = ['./horse.png', './sheep.png', './monkey.png', './chicken.png', './dog.png', './boar.png']

def get_current_time():
    current_time = time.localtime()

    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec

    return hour, minute, second

def draw_tic_marks():
    
    # 午前午後の判断
    hour, _, _ = get_current_time()
    if hour <= 11 or hour == 23:
        am_pm = am
    else:
        am_pm = pm
    
    for i in range(60):
        # 目盛りの角度を計算
        angle = math.radians(6*i-90)
        
        # 目盛りの始点座標
        if i % 5 == 0:
            start = CLOCK_FACE_RADIUS * 0.875
        else:
            start = CLOCK_FACE_RADIUS * 0.925
        
        start_x = start * math.cos(angle) + CENTER
        start_y = start * math.sin(angle) + CENTER
        
        # 目盛りの終点座標
        end = CLOCK_FACE_RADIUS
        
        end_x = end * math.cos(angle) + CENTER
        end_y = end * math.sin(angle) + CENTER
        
        # 目盛りの太さ
        line_width = CLOCK_FACE_RADIUS * 0.01
        
        # 目盛りの色
        if i % 5 == 0 and i % 10 != 0:
            color = '#000000'
        else:
            color = '#ffffff'
        
        # 目盛りの描画
        canvas.create_line(
            start_x, start_y, end_x, end_y,
            width = line_width, fill = color
        )
        
        # 動物の表示
        if i % 10 == 0:
            animal = am_pm[int(i/10)]
            pil_image = Image.open(animal)
            pil_image = pil_image.resize((int(SIDE/8), int(SIDE/8)), Image.LANCZOS)
            img_animal = ImageTk.PhotoImage(pil_image)
            animal_images.append(img_animal)    # リストに追加して参照を保持
            animal_x = CENTER + CLOCK_FACE_RADIUS*0.85*math.cos(angle)
            animal_y = CENTER + CLOCK_FACE_RADIUS*0.85*math.sin(angle)
            canvas.create_image(animal_x, animal_y, image = img_animal)
                        

def tick():
    # 現在時刻の取得
    hour, minute, second = get_current_time()

    # 針の角度の計算
    hour_angle = math.radians((hour * 30) + (minute * 0.5) - 90)
    minute_angle = math.radians((minute * 6) + (second * 0.1) - 90)
    second_angle = math.radians(second * 6 - 90)

    # 針の長さ
    hour_hand_length = CLOCK_FACE_RADIUS * 0.5
    minute_hand_length = CLOCK_FACE_RADIUS * 0.6
    second_hand_length = CLOCK_FACE_RADIUS * 0.6

    # 時針の移動
    canvas.coords(
        hour_hand,
        CENTER,
        CENTER,
        hour_hand_length * math.cos(hour_angle) + CENTER,
        hour_hand_length * math.sin(hour_angle) + CENTER,
    )

    # 分針の移動
    canvas.coords(
        minute_hand,
        CENTER,
        CENTER,
        minute_hand_length * math.cos(minute_angle) + CENTER,
        minute_hand_length * math.sin(minute_angle) + CENTER,
    )

    # 秒針の移動
    canvas.coords(
        second_hand,
        CENTER,
        CENTER,
        second_hand_length * math.cos(second_angle) + CENTER,
        second_hand_length * math.sin(second_angle) + CENTER,
    )
    
    root.title(str(hour) + ':' + str(minute) + ':' + str(second))
    root.after(1000, tick)

draw_tic_marks()
tick()
root.mainloop()