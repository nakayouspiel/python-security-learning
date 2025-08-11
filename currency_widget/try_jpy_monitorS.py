import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
import tkinter as tk
from tkinter import simpledialog

# 前日を基準に色を判断するため、前日の終値の1桁目を保存する箱
# 今日の基準値を6として初期化
previous_day_baseline = 6
# スレッドごとに独立したデータを保存する箱
thread_data = threading.local()

# 設定するパスワードを定義
SECRET_PASSWORD = "1234"

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

# 終了処理用の関数
def on_quit(icon):
    icon.stop()

# 起動時のパスワード認証を行う関数
def authenticate_on_startup():
    # Tkinterのルートウィンドウを作成し、非表示にする
    root = tk.Tk()
    root.withdraw()

    # パスワード入力ダイアログを表示
    password = simpledialog.askstring("パスワード入力", "アプリケーションを開始するにはパスワードを入力してください:", show='*')

    return password == SECRET_PASSWORD

# メイン処理
if __name__ == '__main__':
    if authenticate_on_startup():
        icon_image = create_image("0.000")
        menu = (pystray.MenuItem('終了', on_quit),)
        icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
        
        thread = threading.Thread(target=update_rate, args=(icon,))
        thread.daemon = True
        thread.start()
        
        icon.run()
    else:
        # パスワードが間違っている場合、アプリケーションを終了
        print("パスワードが違います。アプリケーションを終了します。")