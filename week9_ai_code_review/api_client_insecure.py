import requests
import json
import sys

# プログラム実行時に与えられる引数（入力）が十分かチェック
if len(sys.argv) < 2:
    print("使い方: python api_client_insecure.py <ユーザーID (1-10)>")
    sys.exit(1)

# ここから修正！ユーザー入力を検証する
user_id_str = sys.argv[1]

# 入力が数字であるか、そして有効な範囲内であるかをチェック
if not user_id_str.isdigit():
    print("エラー: ユーザーIDは数字で入力してください。")
    sys.exit(1)

user_id = int(user_id_str)

if not 1 <= user_id <= 10:
    print("エラー: ユーザーIDは1から10の範囲で入力してください。")
    sys.exit(1)
    
# 検証が通った安全なuser_idだけをURLに組み込む
api_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"

# 2. Web APIにアクセスしてデータを取得
print("--- Web APIにアクセスしてデータを取得 ---")
try:
    response = requests.get(api_url)
    response.raise_for_status()

    user_data = response.json()
    print(f"成功: {api_url} からJSONデータを取得しました。")

    # 3. 取得したデータを辞書として表示
    print("\n--- ユーザーデータを辞書として表示 ---")
    print(f"ユーザーID: {user_data['id']}")
    print(f"ユーザー名: {user_data['name']}")
    print(f"メールアドレス: {user_data['email']}")
    print(f"住所: {user_data['address']['city']}")

except requests.exceptions.RequestException as e:
    print(f"エラー: {e}")
    print("ネットワーク接続またはAPIのURLに問題がある可能性があります。")
except KeyError as e:
    print(f"エラー: JSONデータに期待するキーが見つかりませんでした。- {e}")

print("\n--- APIクライアント処理が完了しました ---")