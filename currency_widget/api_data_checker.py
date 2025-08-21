import requests
import json

API_ENDPOINT = "https://forex-api.coin.z.com/public"
PATH = "/v1/ticker"

try:
    # APIにリクエストを送信
    response = requests.get(API_ENDPOINT + PATH)
    response.raise_for_status() # HTTPエラーが発生した場合に例外を投げる
    
    # 応答が成功したらJSONを解析
    api_data = response.json()
    
    print("APIから取得したデータ構造：")
    # 整形して表示することで、データの階層が分かりやすくなる
    print(json.dumps(api_data, indent=2))
    '''
    # TRY/JPYのデータを特定し、bid価格を表示
    for ticker in api_data["data"]:
        if ticker["symbol"] == "TRY_JPY":
            print("\nTRY_JPYの価格情報：")
            print(f"シンボル: {ticker['symbol']}")
            print(f"現在価格（bid）: {ticker['bid']}")
            break

except requests.exceptions.RequestException as e:
    print(f"通信エラーが発生しました: {e}")
except json.JSONDecodeError:
    print("JSONデータの解析に失敗しました。")
except KeyError as e:
    print(f"キーが見つかりません: {e}")   '''