# 変数の定義と計算
num1 = 15
num2 = 7
result_add = num1 + num2
print(f"足し算の結果: {result_add}")

#　文字列の操作
first_name = "youhei"
last_name = "nakamura"
full_name = first_name + " " + last_name    
print(f"フルネーム: {full_name}")

#【f-stringを使った文字列結合の例（Copilotが提案したもの）】
full_name_fstring = f"{first_name} {last_name}"
print(f"フルネーム: {full_name_fstring}")

# リストの作成とアクセス
# 角括弧 [] を使って作成します。リストは要素の順序があり、後から変更（追加・削除・変更）が可能です。
fruits = ["apple", "banana", "cherry"] # リストの作成
print(f"\n--- リストの練習 ---") # 区切り線を追加
print(f"初期リスト: {fruits}")
print(f"リストの最初の要素: {fruits[0]}") # インデックス0でアクセス（Pythonのインデックスは0から始まります）

# リストに新しい要素を追加
fruits.append("orange") # リストの末尾に"orange"を追加
print(f"リストに要素を追加後: {fruits}")

# リストの特定の要素を変更
fruits[1] = "grape" # インデックス1の要素を"banana"から"grape"に変更
print(f"リストの要素変更後: {fruits}")

# リストから要素を削除
fruits.remove("apple") # "apple"という値を指定して削除
print(f"リストから'apple'を削除後: {fruits}")

# 条件分岐
# 条件に応じて処理を切り替えるための構文です。
print(f"\n--- 条件分岐の練習 ---") # 区切り線を追加
score = 69 # この点数を色々と変更して、実行結果を確認してみてください (例: 95, 60, 75など)

if score >= 90: # もし score が90以上なら、この下の行が実行されます
    print(f"あなたのスコアは {score} 点です。評価: 優")
elif score >= 70: # 90未満で、かつ score が70以上なら、この下の行が実行されます
    print(f"あなたのスコアは {score} 点です。評価: 良")
else: # それ以外（score が70未満）なら、この下の行が実行されます
    print(f"あなたのスコアは {score} 点です。評価: 可")

# 別な条件分岐の例
temperature = 31 # 現在の気温を想定 (例: 15, 25, 32など)
if temperature > 30:
    print("今日は非常に暑いので、熱中症に注意してください！")
elif temperature > 25:
    print("今日は暑いです。水分補給を心がけましょう。")
else:
    print("過ごしやすい一日です。")

# 【追加練習】タプルとセット
# タプルの作成とアクセス（変更不可なリストのようなもの）
# 丸括弧 () を使って作成します。要素の順序はありますが、一度作成したら要素の追加・削除・変更はできません。
coordinates = (10, 20)
print(f"\n--- タプルとセットの練習 ---") # 区切り線を追加
print(f"座標: x={coordinates[0]}, y={coordinates[1]}") # インデックスでアクセス
# 注意：タプルは一度作成したら要素の追加や変更はできません。
# 例：coordinates.append(30) や coordinates[0] = 5 はエラーになります。試してみるのも良い経験です。

# セットの作成と操作（重複を許さない集合、順序なし）
# 波括弧 {} を使って作成しますが、辞書とは異なりキーと値のペアではありません。順序は保証されません。
numbers = {1, 2, 3, 2, 4} # 重複する2は自動的に1つになります（{1, 2, 3, 4} のようになる）
print(f"初期セット: {numbers}")
numbers.add(5) # 要素を追加
print(f"セットに5を追加: {numbers}")
numbers.add(3) # 既に存在する3を追加しても変化なし
print(f"セットに既存の3を追加: {numbers}")
numbers.remove(1) # 要素を削除
print(f"セットから1を削除: {numbers}")

# 【追加練習】辞書（dict）の操作
# 辞書の作成とアクセス（キーと値のペアでデータを管理）
# 波括弧 {} を使い、キー: 値 の形式で記述します。キーは一意である必要があります。
print(f"\n--- 辞書の練習 ---") # 区切り線を追加
user_info = {
    "name": "Spiel", # あなたの名前に変更してもOK
    "age": 42,       # あなたの年齢に設定してもOK
    "city": "Nanjo", # あなたの居住地（例: Yaese, Okinawa）に設定してもOK
    "occupation": "Care Manager" # あなたの職業に設定してもOK
}
print(f"ユーザー名: {user_info['name']}") # キーを使って値にアクセス
print(f"年齢: {user_info['age']}")
print(f"在住地: {user_info['city']}") # 残りの情報を表示


# 辞書に新しいキーと値を追加
user_info['hobby'] = "PC building" # あなたの趣味を追加
print(f"新しい趣味: {user_info['hobby']}")

# 既存のキーの値を更新
user_info['age'] = 43 # 例：年齢を更新
print(f"更新後の年齢: {user_info['age']}")

# 辞書からキーと値を削除
del user_info['occupation'] # 'occupation'キーとその値を削除
print(f"職業削除後の情報: {user_info}")


# 辞書をforループで処理する様々な方法
# 辞書はループと組み合わせて使われることが非常に多いです。
print(f"\n--- 辞書とループの練習 ---") # 区切り線を追加

# 辞書の全てのキーと値を出力（.items()メソッドの活用）
print("現在のユーザー情報（キーと値）:")
for key, value in user_info.items(): # .items()はキーと値のペアをタプルとして返す
    print(f"  {key}: {value}")

# 辞書のキーだけを出力（.keys()メソッドの活用）
print("\nユーザー情報のキーだけ:")
for key in user_info.keys(): # .keys()はキーだけを返す
    print(f"  - {key}")

# 辞書の値だけを出力（.values()メソッドの活用）
print("\nユーザー情報の値だけ:")
for value in user_info.values(): # .values()は値だけを返す
    print(f"  - {value}")

# リストをforループで処理する（リストの各要素に順にアクセス）
print(f"\n--- リストとループの練習 ---") # 区切り線を追加
colors = ["red", "green", "blue"]
for color in colors:
    print(f"色: {color}")

# whileループの練習（条件が真である限り繰り返す）
print(f"\n--- whileループの練習 ---") # 区切り線を追加
count = 0 # カウンターを初期化
while count < 3: # countが3より小さい間はループを続ける
    print(f"カウント: {count}")
    count += 1 # countを1増やすのを忘れないこと！ (これを忘れると無限ループになります)

    