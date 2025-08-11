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
        # GMOコインの仮想通貨APIのエンドポイント
        API_ENDPOINT = "https://api.coin.z.com/public/v1/ticker"
        
        # APIにリクエストを送る
        response = requests.get(API_ENDPOINT, params={"symbol": "BTC_JPY"})
        
        try:
            api_data = response.json()

            if api_data["status"] == 0:
                all_tickers = api_data["data"]
                btc_info = None
                
                if all_tickers:
                    btc_info = all_tickers[0]
                
                if btc_info:
                    bid_price_str = btc_info["bid"]
                    
                    price_in_manen = int(decimal.Decimal(bid_price_str) / 10000)
                    price_text = str(price_in_manen)
                    
                    icon.icon = create_image(price_text)
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
def create_image(text):
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()
    
    # 4桁の数字を2つに分割
    if len(text) == 4:
        first_two_digits = text[:2]
        last_two_digits = text[2:]
        
        # 上段に最初の2桁を描画
        dc.text((32, 10), first_two_digits, font=font, fill=(0, 0, 0), anchor='mm')
        # 下段に最後の2桁を描画
        dc.text((32, 45), last_two_digits, font=font, fill=(0, 0, 0), anchor='mm')
    else:
        # 4桁以外の数字の場合はそのまま描画
        bbox = dc.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        dc.text((x, y), text, font=font, fill=(0, 0, 0))
    
    return image

# 終了処理用の関数
def on_quit(icon):
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    icon_image = create_image("...")
    menu = (pystray.MenuItem('終了', on_quit),)
    icon = pystray.Icon("exchange_rate_tray", icon_image, "BTCレート", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon,))
    thread.daemon = True
    thread.start()
    
    icon.run()