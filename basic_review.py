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