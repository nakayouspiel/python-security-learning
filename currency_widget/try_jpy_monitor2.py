"""
# トルコリラ/円 為替レート監視ツール

## 概要
このスクリプトは、PCのタスクトレイに常駐し、トルコリラ/円TRY/JPYの為替レート変動をリアルタイムで監視するツールです。

## 主な機能
1.  **基準価格の自動/手動設定**
    * **起動時**: 前日の終値を手動で入力することで、その日の基準価格を設定できます。
    * **日足切り替わり時**: 日付が変わると自動的に基準価格がリセットされ、その日の最初の価格を新しい基準として更新します。
2.  **複数の表示モード**
    * 「小数点2,3桁」「小数点1,2桁」では、基準価格からの差額を表示します。
    * 「現在値（銭）」では、現在の価格そのものを分かりやすく表示します。
3.  **タスクスケジューラとの連携**
    * PCの電源設定と連携し、タスクスケジューラで日足確定時刻にPCを自動起動させることで、効率的な運用が可能です。

## 注意事項
* 手動で基準価格を入力しない場合、その日の最初の価格が自動で基準となります。
* このツールには、PCを自動でスリープさせる機能は含まれていません。
"""


import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
from threading import Event
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

# プログラムの先頭に追加
# 表示モードを管理するグローバル変数
# 0: 小数点以下2,3桁, 1: 小数点以下1,2桁, 2: 現在値（銭）
display_mode = 0

# 日付が変わるたびに、その日の最初の価格が自動的にここに設定されます。
previous_day_baseline = decimal.Decimal('0')

# 最後に基準値を更新した日付を保存する箱
last_update_date = None

# メニューから呼び出す関数を定義
def set_display_mode(icon, item):
    global display_mode
    mode = ["小数点２，３", "小数点１，２", "現在値（銭）"].index(item.text)
    display_mode = mode

# 手動で基準値を入力する関数
def initial_baseline_input():
    global previous_day_baseline
    
    root = tk.Tk()
    root.withdraw()
    
    user_input = simpledialog.askstring("基準価格の入力", "前日の終値（基準価格）を入力してください。\n例: 3.620", parent=root)
    
    try:
        if user_input:
            previous_day_baseline = decimal.Decimal(user_input).quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
            print(f"基準価格を手動で {previous_day_baseline} に設定しました。")
        else:
            # 入力がない場合はデフォルトで0を設定
            previous_day_baseline = decimal.Decimal('0')
            print("入力がありませんでした。基準価格は0に設定されます。")

    except (ValueError, decimal.InvalidOperation):
        print("無効な入力です。基準価格は0に設定されます。")
        previous_day_baseline = decimal.Decimal('0')

# 為替レート取得と更新処理を行う関数
def update_rate(icon, stop_event):
    global previous_day_baseline
    global display_mode
    global last_update_date

    API_ENDPOINT = "https://forex-api.coin.z.com/public"
    PATH = "/v1/ticker"
    
    while not stop_event.is_set():
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
                    current_date_str = try_jpy_info["timestamp"].split('T')[0]
                    current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
                    
                    if last_update_date is None or last_update_date != current_date:
                        last_update_date = current_date
                        if previous_day_baseline == decimal.Decimal('0'): # 初回起動時やリセット後に手動入力がない場合の処理
                            previous_day_baseline = decimal.Decimal('0') # 基準値を0に設定
                        
                    bid_price_decimal = decimal.Decimal(try_jpy_info["bid"])
                    
                    if previous_day_baseline == decimal.Decimal('0'):
                        # 日付が変わった最初の価格を基準値として自動設定
                        if last_update_date == current_date:
                            previous_day_baseline = bid_price_decimal.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)


                    main_digits = ""
                    difference = decimal.Decimal('0')
                    
                    if display_mode == 2:
                        rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.1'), rounding=decimal.ROUND_HALF_UP)
                        main_digits = str(int(rounded_price * 10))
                        fill_color = (0, 0, 0)
                    else:
                        difference = bid_price_decimal - previous_day_baseline
                        
                        if display_mode == 0:
                            rounded_diff = difference.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
                            main_digits = str(int(rounded_diff * 1000))
                        elif display_mode == 1:
                            rounded_diff = difference.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
                            main_digits = str(int(rounded_diff * 100))

                        if main_digits == "0":
                            main_digits = "0"
                            difference = decimal.Decimal('0')
                        elif main_digits.startswith('-'):
                            main_digits = main_digits.lstrip('-')
                            difference = -difference
                    
                        fill_color = (0, 0, 0)
                        if difference > 0:
                            fill_color = (255, 0, 0)
                        elif difference < 0:
                            fill_color = (173, 216, 230)
                    
                    icon.icon = create_image(main_digits, fill_color)
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
    
    if text in ["ERR", "NET"]:
        try:
            error_font = ImageFont.truetype("arial.ttf", 25)
            dc.text((32, 32), text, font=error_font, fill=fill_color, anchor='mm')
        except IOError:
            error_font = ImageFont.load_default()
            dc.text((32, 32), text, font=error_font, fill=fill_color, anchor='mm')
    else:
        try:
            main_font = ImageFont.truetype("arial.ttf", 60)
            dc.text((32, 32), text, font=main_font, fill=fill_color, anchor='mm')
        except IOError:
            main_font = ImageFont.load_default()
            dc.text((32, 32), text, font=main_font, fill=fill_color, anchor='mm')
    
    return image

# 終了処理用の関数
def on_quit(icon, stop_event):
    stop_event.set()
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    # 起動時に手動入力を促す
    initial_baseline_input()

    icon_image = create_image("0")
    stop_event = Event()
    menu = pystray.Menu(
        pystray.MenuItem(
            "小数点２，３",
            lambda icon, item: set_display_mode(icon, item),
            checked=lambda item: display_mode == 0
        ),
        pystray.MenuItem(
            "小数点１，２",
            lambda icon, item: set_display_mode(icon, item),
            checked=lambda item: display_mode == 1
        ),
        pystray.MenuItem(
            "現在値（銭）",
            lambda icon, item: set_display_mode(icon, item),
            checked=lambda item: display_mode == 2
        ),
        pystray.MenuItem('終了', lambda icon: on_quit(icon, stop_event))
    )
    
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon, stop_event))
    thread.daemon = True
    thread.start()
    
    icon.run()