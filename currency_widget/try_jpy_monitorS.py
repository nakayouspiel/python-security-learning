import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 前日を基準に色を判断するため、前日の終値の1桁目を保存する箱
# 今日の基準値を6として初期化
previous_day_baseline = 6
# スレッドごとに独立したデータを保存する箱
thread_data = threading.local()

# 為替レートの履歴を保存するリスト
rate_history = []

# 為替レート取得と更新処理を行う関数
def update_rate(icon):
    global previous_day_baseline
    thread_data.last_rate = None
    
    while True:
        API_ENDPOINT = "https://forex-api.coin.z.com/public"
        PATH = "/v1/ticker"
        
        response = requests.get(API_ENDPOINT + PATH)
        
        try:
            api_data = response.json()
            if api_data["status"] == 0:
                all_tickers = api_data["data"]
                try_jpy_info = None
                for ticker in all_tickers:
                    if ticker["symbol"] == "TRY_JPY":
                        try_jpy_info = ticker
                        break
                
                if try_jpy_info:
                    bid_price_decimal = decimal.Decimal(try_jpy_info["bid"])
                    rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
                    
                    sen_full_str = str(rounded_price).split('.')[1]
                    first_sen_digit = int(sen_full_str[0])
                    
                    fill_color = (0, 0, 0)
                    if first_sen_digit > previous_day_baseline:
                        fill_color = (255, 0, 0)
                    elif first_sen_digit < previous_day_baseline:
                        fill_color = (0, 191, 255)
                    
                    if first_sen_digit != previous_day_baseline:
                        previous_day_baseline = first_sen_digit
                    
                    # 💡 ここを修正しました: float型に変換
                    rate_history.append(float(rounded_price))
                    if len(rate_history) > 100:
                        rate_history.pop(0)

                    thread_data.last_rate = rounded_price
                    icon.icon = create_image(str(rounded_price), fill_color)
                else:
                    icon.icon = create_image("ERR")
            else:
                icon.icon = create_image("ERR")

        except requests.exceptions.RequestException:
            icon.icon = create_image("NET")
        except (json.JSONDecodeError, KeyError):
            icon.icon = create_image("ERR")

        time.sleep(5)

# アイコンを作成する関数
def create_image(text, fill_color=(0, 0, 0)):
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    try:
        main_font = ImageFont.truetype("arial.ttf", 60)
        sub_font = ImageFont.truetype("arial.ttf", 25)
    except IOError:
        main_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        
    if '.' in text:
        yen, sen_full = text.split('.')
    else:
        yen = text
        sen_full = "000"

    main_digits = sen_full[1:3]
    dc.text((32, 32), main_digits, font=main_font, fill=fill_color, anchor='mm')
    
    return image

# グラフを表示する関数
def show_graph(icon):
    if not rate_history:
        return
    
    root = tk.Tk()
    root.title("為替レートグラフ")
    # 💡 ウィンドウを閉じる際に呼ばれる関数を設定
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(rate_history)
    ax.set_title("TRY/JPY 為替レート変動")
    ax.set_xlabel("更新回数")
    ax.set_ylabel("為替レート")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

# 終了処理用の関数
def on_quit(icon):
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    icon_image = create_image("0.000")
    menu = (pystray.MenuItem('グラフ表示', show_graph), pystray.MenuItem('終了', on_quit))
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon,))
    thread.daemon = True
    thread.start()
    
    icon.run()