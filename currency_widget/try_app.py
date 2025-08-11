import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading

# 為替レート取得と更新処理を行う関数
def update_rate(icon):
    # 無限ループで定期的にレートを更新
    while True:
        # GMOコインのFX APIのエンドポイント
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
                    bid_price_str = try_jpy_info["bid"]
                    bid_price_decimal = decimal.Decimal(bid_price_str)
                    rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
                    
                    icon.icon = create_image(str(rounded_price))
                else:
                    icon.icon = create_image("ERR")
            else:
                icon.icon = create_image("ERR")
        except requests.exceptions.RequestException:
            icon.icon = create_image("NET")
        except (json.JSONDecodeError, KeyError):
            icon.icon = create_image("ERR")

        time.sleep(30)

# タスクバーに表示するアイコンを作成する関数
def create_image(text):
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)

    # フォントの指定
    try:
        font = ImageFont.truetype("arial.ttf", 60) # 銭の部分を大きく
    except IOError:
        font = ImageFont.load_default()
        
    # 文字列を円と銭に分割
    if '.' in text:
        yen, sen = text.split('.')
    else:
        yen = text
        sen = "00"

    # 銭の部分を大きく中央に描画
    dc.text((32, 32), sen, font=font, fill=(0, 0, 0), anchor='mm')
    
    return image

# 終了処理用の関数
def on_quit(icon):
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    icon_image = create_image("0.00")
    menu = (pystray.MenuItem('終了', on_quit),)
    icon = pystray.Icon("exchange_rate_tray", icon_image, "為替レート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon,))
    thread.daemon = True
    thread.start()
    
    icon.run()