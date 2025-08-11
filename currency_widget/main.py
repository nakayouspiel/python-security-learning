import requests
import json
import decimal
import time # ← この行を追加

# GMOコインのFX APIのエンドポイント
API_ENDPOINT = "https://forex-api.coin.z.com/public"
PATH = "/v1/ticker"

# 無限ループの開始
while True:
    response = requests.get(API_ENDPOINT + PATH)
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
            
            # 画面表示を1行でシンプルにする
            print(f"TRY/JPY: {rounded_price}")
        else:
            print("TRY/JPYのデータが見つかりませんでした。")
    else:
        print(f"APIからの応答が失敗しました。ステータス: {api_data['status']}")
        if "messages" in api_data:
            for message in api_data["messages"]:
                print(f"  - エラーコード: {message['message_code']}, メッセージ: {message['message_string']}")
    
    # 5秒間プログラムを一時停止
    time.sleep(30)