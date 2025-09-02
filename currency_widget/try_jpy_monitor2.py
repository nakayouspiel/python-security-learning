import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
from threading import Event

# 表示モードを管理するグローバル変数
# 0: 小数点以下3桁 (TRY/JPY), 1: 小数点以下2桁 (USD/JPY)
display_mode = 0

# 選択通貨を管理するグローバル変数
selected_currency = "TRY_JPY"

# --- 変更: 前回値を保存するグローバル変数 ---
last_price = decimal.Decimal('0')

# メニューから呼び出す関数を定義
def set_currency(icon, item):
    global selected_currency
    global display_mode
    global last_price
    
    if item.text == "TRY/JPY":
        selected_currency = "TRY_JPY"
        display_mode = 0
    elif item.text == "USD/JPY":
        selected_currency = "USD_JPY"
        display_mode = 1
    
    last_price = decimal.Decimal('0')

# 為替レート取得と更新処理を行う関数
def update_rate(icon, stop_event):
    global last_price
    
    while not stop_event.is_set():
        API_ENDPOINT = "https://forex-api.coin.z.com/public"
        PATH = "/v1/ticker"
        
        try:
            response = requests.get(API_ENDPOINT + PATH)
            api_data = response.json()
            if api_data["status"] == 0:
                all_tickers = api_data["data"]
                selected_info = None
                for ticker in all_tickers:
                    if ticker["symbol"] == selected_currency:
                        selected_info = ticker
                        break
                
                if selected_info:
                    bid_price_decimal = decimal.Decimal(selected_info["bid"])

                    if display_mode == 0:
                        rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
                    else:
                        rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
                    
                    # --- 変更: 前回値と比較して色を決定 ---
                    fill_color = (0, 0, 0)
                    if last_price != decimal.Decimal('0'):
                        if rounded_price > last_price:
                            fill_color = (255, 0, 0) # 赤
                        elif rounded_price < last_price:
                            fill_color = (0, 191, 255) # 水色
                    
                    # 今回の値を次回の比較のために保存
                    last_price = rounded_price
                    
                    
                    # 表示するテキストを準備
                    sen_full = str(rounded_price).split('.')[1]
                    if len(sen_full) == 2: # ドル円の場合
                        text_to_display = sen_full[0:2]
                    else: # リラ円の場合
                        text_to_display = sen_full[1:3]

                    icon.icon = create_image(text_to_display, fill_color)
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
    icon_image = create_image("000")
    stop_event = Event()
    
    selected_currency = "TRY_JPY"
    
    menu = pystray.Menu(
        pystray.MenuItem(
            "Currency",
            pystray.Menu(
                pystray.MenuItem("TRY/JPY", lambda icon, item: set_currency(icon, item), checked=lambda item: selected_currency == "TRY_JPY"),
                pystray.MenuItem("USD/JPY", lambda icon, item: set_currency(icon, item), checked=lambda item: selected_currency == "USD_JPY")
            )
        ),
        pystray.MenuItem('終了', lambda icon: on_quit(icon, stop_event))
    )
    
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon, stop_event))
    thread.daemon = True
    thread.start()
    
    icon.run()