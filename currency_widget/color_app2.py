import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading

# スレッドごとに独立したデータを保存する箱
thread_data = threading.local()

# 為替レート取得と更新処理を行う関数
def update_rate(icon):
    # スレッドごとのlast_rateを初期化
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
                    # 小数点以下3桁まで取得
                    rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
                    
                    # 小数点以下の部分を取得し、整数に変換
                    sen_full_str = str(rounded_price).split('.')[1]
                    first_sen_digit = int(sen_full_str[0])
                    
                    # 最初の1桁に基づいて色を決定
                    fill_color = (0, 0, 0) # デフォルトは黒
                    if first_sen_digit > 6:
                        fill_color = (255, 0, 0) # 6より大きければ赤
                    elif first_sen_digit < 6:
                        fill_color = (0, 191, 255) # 6より小さければ水色
                    
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
        main_font = ImageFont.truetype("arial.ttf", 60) # 下2桁用の大きなフォント
        sub_font = ImageFont.truetype("arial.ttf", 25) # 上1桁用の小さなフォント
    except IOError:
        main_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        
    # 文字列を円と銭に分割
    if '.' in text:
        yen, sen_full = text.split('.')
    else:
        yen = text
        sen_full = "000"

    # 銭の部分の表示ロジック
    if len(sen_full) >= 3:
        main_digits = sen_full[1:3] # 2桁目と3桁目を取得 (例: "15")
        
        # 下2桁を大きく中央に描画
        dc.text((32, 32), main_digits, font=main_font, fill=fill_color, anchor='mm')
    else:
        # 3桁未満の場合は、全体を大きく中央に描画
        dc.text((32, 32), sen_full, font=main_font, fill=fill_color, anchor='mm')
    
    return image

# 終了処理用の関数
def on_quit(icon):
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    icon_image = create_image("0.000")
    menu = (pystray.MenuItem('終了', on_quit),)
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon,))
    thread.daemon = True
    thread.start()
    
    icon.run()