import requests
import json
import decimal

# Yahoo!ファイナンスのAPIエンドポイント
API_ENDPOINT = "https://query2.finance.yahoo.com/v8/finance/chart/TRYJPY=X"

# APIにリクエストを送る
# Yahoo!ファイナンスの場合、paramsは不要
response = requests.get(API_ENDPOINT)

if response.status_code == 200:
    api_data = response.json()

    # 応答データから価格情報のある部分を抽出
    try:
        # dataリストの最初の要素（辞書）を取得
        ticker_info = api_data["chart"]["result"][0]

        # 現在の価格（bid）を取得
        current_price_str = str(ticker_info["meta"]["regularMarketPrice"])

        # 小数点以下2桁に丸める
        bid_price_decimal = decimal.Decimal(current_price_str)
        rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
        
        print(f"TRY/JPY: {rounded_price}")

    except KeyError:
        # データが見つからなかった場合
        print("TRY/JPYのデータが見つかりませんでした。")
        print("APIからの応答内容を以下に表示します:")
        print(json.dumps(api_data, indent=2))

else:
    print(f"データの取得に失敗しました。ステータスコード: {response.status_code}")