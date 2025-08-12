import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
import tkinter as tk

plt.rcParams['font.family'] = 'MS Gothic'
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# 日本語フォントを使用するための設定
import matplotlib.pyplot as plt

# 前日を基準に色を判断するため、前日の終値の1桁目を保存する箱
# 今日の基準値を6として初期化
previous_day_baseline = 6
# スレッドごとに独立したデータを保存する箱
thread_data = threading.local()

# グラフ表示用に為替レートの履歴を保存するリスト
rate_history = []
# アプリ起動時のレートを基準として保存する変数
previous_day_close = 0.0

# 為替レート取得と更新処理を行う関数
def update_rate(icon):
    global previous_day_baseline, previous_day_close
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
                    
                    # 💡ここから新しい変更
                    # アプリ起動後、初めて値を取得した時だけ基準値として保存
                    if previous_day_close == 0.0:
                        previous_day_close = float(rounded_price)

                    # 現在値と基準値の差を計算し、1000倍して整数に変換
                    difference = int((float(rounded_price) - previous_day_close) * 1000)
                    
                    # アイコンに表示するテキストを差額にする
                    icon_text = str(difference)
                    
                    # アイコンの色を差額に基づいて決定
                    fill_color = (0, 0, 0)
                    if difference > 0:
                        fill_color = (255, 0, 0) # 赤
                    elif difference < 0:
                        fill_color = (0, 191, 255) # 水色
                    # 💡ここまで新しい変更

                    # 取得した為替レートを履歴リストに追加
                    rate_history.append(float(rounded_price))
                    # 履歴リストのサイズを制限（最新の100個のみ保持）
                    if len(rate_history) > 100:
                        rate_history.pop(0)

                    thread_data.last_rate = rounded_price
                    icon.icon = create_image(icon_text, fill_color)
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
        
    # 💡ここから新しい変更
    # テキストの幅を計算し、中央に配置
    text_width = dc.textlength(text, font=main_font)
    text_x = (width - text_width) / 2
    dc.text((text_x, 32), text, font=main_font, fill=fill_color, anchor='mm')
    # 💡ここまで新しい変更
    
    return image

# グラフを表示する関数
def show_graph(icon):
    if not rate_history:
        return
    
    root = tk.Tk()
    root.title("為替レートグラフ")
    # ウィンドウを閉じる際に呼ばれる関数を設定
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
    # メニューに「グラフ表示」を追加
    menu = (pystray.MenuItem('グラフ表示', show_graph), pystray.MenuItem('終了', on_quit))
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon,))
    thread.daemon = True
    thread.start()
    
    icon.run()