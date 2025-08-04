import requests
import json # JSONデータを扱うための標準ライブラリ
from pathlib import Path

# 1. Web APIのURLを指定
# このAPIは、ダミーのユーザーデータをJSON形式で提供します。
# Webスクレイピングと異なり、HTMLではなくデータそのものを取得します。
print("--- Web APIにアクセスしてデータを取得 ---")
api_url = "https://jsonplaceholder.typicode.com/users/1"

try:
    # requests.get() でWeb APIにアクセス
    response = requests.get(api_url)
    response.raise_for_status() # HTTPステータスコードが200番台でなければ例外を発生させる

    # 2. 取得したデータをJSON形式で解析
    # requestsライブラリは、JSON形式の応答を自動的にPythonの辞書に変換する機能を持っています。
    user_data = response.json()

    print(f"成功: {api_url} からJSONデータを取得しました。")

    # JSONデータをPythonの辞書として扱う
    print("\n--- ユーザーデータを辞書として表示 ---")
    # Pythonの辞書（dict）として、キーを使って値にアクセスできます。
    # 辞書の操作は、第1ヶ月目で学習しましたね！
    print(f"ユーザーID: {user_data['id']}")
    print(f"ユーザー名: {user_data['name']}")
    print(f"メールアドレス: {user_data['email']}")
    print(f"住所: {user_data['address']['city']}") # 辞書の中の辞書にアクセス

    # 辞書全体を見たい場合は、pprintモジュールを使うと見やすくなります。
    # print("\n--- 辞書データ全体 ---")
    # import pprint
    # pprint.pprint(user_data)

except requests.exceptions.RequestException as e:
    print(f"エラー: {e}")
    print("ネットワーク接続またはAPIのURLに問題がある可能性があります。")
except KeyError as e:
    print(f"エラー: JSONデータに期待するキーが見つかりませんでした。- {e}")

print("\n--- APIクライアント処理が完了しました ---")