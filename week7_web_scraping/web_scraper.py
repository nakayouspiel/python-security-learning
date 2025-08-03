import requests
from bs4 import BeautifulSoup

# 1. Webサイトからの情報取得 (requestsライブラリ)
# requestsライブラリは、HTTP通信を非常に簡単に扱えるように作られています。
print("--- requestsライブラリを使ってWebサイトにアクセス ---")
url = "https://ja.wikipedia.org/wiki/Python"

try:
    response = requests.get(url) # GETリクエストを送信
    response.raise_for_status() # HTTPステータスコードが200番台でなければ例外を発生させる

    print(f"成功: {url} からの応答を取得しました。")
    print(f"ステータスコード: {response.status_code}")
    # print(f"レスポンスヘッダー:\n{response.headers}") # ヘッダーを表示したい場合はコメントアウトを解除
    print(f"レスポンスの文字コード: {response.encoding}")

    # 2. 取得したHTMLコードから情報を解析 (BeautifulSoupライブラリ)
    # BeautifulSoupは、HTMLやXMLのようなマークアップ言語の解析を簡単に行うためのライブラリです。
    print("\n--- BeautifulSoupを使ってHTMLを解析 ---")
    soup = BeautifulSoup(response.text, 'html.parser')

    # 例1：ページのタイトルを取得
    title = soup.title.string
    print(f"ページのタイトル: {title}")

    # 例2：特定のタグ（見出しなど）のテキストを取得
    # soup.find('h1') で、最初のh1タグを見つけます。
    h1_tag = soup.find('h1')
    print(f"メインの見出し: {h1_tag.text}")

    # 例3：特定のIDを持つ要素のテキストを取得
    # id="mw-headline"を持つ要素（見出し）を探します。
    headline = soup.find(id="mw-headline")
    if headline:
        print(f"見出し（ID 'mw-headline'）: {headline.text}")
    
    # 例4：特定のクラスを持つ要素のリストを取得
    # soup.find_all('p') で、すべてのpタグ（段落）をリストで取得します。
    first_paragraph = soup.find('p').text
    print(f"最初の段落のテキスト:\n{first_paragraph[:150]}...") # 長すぎるので最初の150文字だけ表示

except requests.exceptions.RequestException as e:
    print(f"エラー: {e}")
    print("ネットワーク接続またはURLに問題がある可能性があります。")

print("\n--- ウェブスクレイピング処理が完了しました ---")