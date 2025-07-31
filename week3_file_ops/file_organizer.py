import os
from pathlib import Path

# --- 1. ファイルとフォルダの存在確認 ---
print("--- 1. ファイルとフォルダの存在確認 ---")
file_name = "test_file.txt"
folder_name = "new_folder_for_files" # フォルダ名が重複しないように変更

# os.path.exists() を使った確認
# 指定したパスにファイルやフォルダが存在するかどうかを真偽値（True/False）で返します。
print(f"'{file_name}' は存在しますか？ (os.path.exists): {os.path.exists(file_name)}")
print(f"'{folder_name}' は存在しますか？ (os.path.exists): {os.path.exists(folder_name)}")

# pathlib.Path.exists() を使った確認
# pathlibはosモジュールよりもモダンでオブジェクト指向的にパスを扱えます。
path_file = Path(file_name)
path_folder = Path(folder_name)
print(f"'{file_name}' は存在しますか？ (Path.exists): {path_file.exists()}")
print(f"'{folder_name}' は存在しますか？ (Path.exists): {path_folder.exists()}")


# --- 2. フォルダの作成 ---
print("\n--- 2. フォルダの作成 ---")
# os.makedirs(パス) は、指定したパスにフォルダを作成します。
# 親フォルダが存在しない場合でも、それらもまとめて作成してくれます。
if not os.path.exists(folder_name): # フォルダがなければ作成
    os.makedirs(folder_name)
    print(f"フォルダ '{folder_name}' を作成しました。")
else:
    print(f"フォルダ '{folder_name}' は既に存在します。")


# --- 3. テキストファイルの書き込み ---
print("\n--- 3. テキストファイルの書き込み ---")
# 'w' モードでファイルを開くと、ファイルが存在しない場合は新規作成され、
# 存在する場合は内容が全て上書きされます。
# encoding="utf-8" は、日本語などを含む文字が正しく扱われるための指定です。
with open(file_name, "w", encoding="utf-8") as f:
    f.write("これはPythonで書かれたテストファイルです。\n")
    f.write("ファイル操作の練習をしています。\n")
    f.write("新しい行を追加しました。\n")
print(f"'{file_name}' に内容を書き込みました。")


# --- 4. テキストファイルの読み込み ---
print("\n--- 4. テキストファイルの読み込み ---")
# 'r' モードでファイルを開くと、読み込み専用になります。
# f.read() はファイルの内容全てを文字列として読み込みます。
if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        content = f.read()
        print(f"'{file_name}' の内容:\n{content}")
else:
    print(f"'{file_name}' が見つかりません。読み込みできませんでした。")


# --- 5. ファイル名の変更 ---
print("\n--- 5. ファイル名の変更 ---")
new_file_name = "renamed_test_file.txt" # 変更後のファイル名
# os.rename(古いパス, 新しいパス) でファイル名を変更します。
if os.path.exists(file_name): # 変更前のファイル名が存在するか確認
    os.rename(file_name, new_file_name)
    print(f"'{file_name}' を '{new_file_name}' に変更しました。")
else:
    # ファイル名が既に変更されているか、存在しない場合の対処
    if os.path.exists(new_file_name):
        print(f"'{file_name}' は既に '{new_file_name}' に変更されています。")
    else:
        print(f"'{file_name}' が見つかりません。名前を変更できませんでした。")


# --- 6. ファイルの移動 ---
print("\n--- 6. ファイルの移動 ---")
# ファイルを別のフォルダへ移動するには、os.rename() を使って新しいパスを指定します。
# os.path.join() は、OSに応じた正しいパスの区切り文字（Windowsなら\、Mac/Linuxなら/）を使ってパスを結合します。
moved_file_path = os.path.join(folder_name, new_file_name) # 移動先の完全なパスを作成
if os.path.exists(new_file_name): # 変更後のファイル名が存在するか確認
    os.rename(new_file_name, moved_file_path) # ファイルを新しい場所に移動
    print(f"'{new_file_name}' を '{folder_name}' フォルダに移動しました。")
else:
    # ファイルが既に移動されているか、存在しない場合の対処
    if os.path.exists(moved_file_path):
        print(f"'{new_file_name}' は既に '{folder_name}' に移動されています。")
    else:
        print(f"'{new_file_name}' が見つかりません。移動できませんでした。")


# --- 7. ファイルの削除 ---
print("\n--- 7. ファイルの削除 ---")
# os.remove(パス) でファイルを削除します。
# 削除する前に、ファイルがまだ存在するか確認するのが安全です。
if os.path.exists(moved_file_path):
    os.remove(moved_file_path)
    print(f"'{moved_file_path}' を削除しました。")
else:
    print(f"'{moved_file_path}' が見つかりません。削除できませんでした。")

# --- 8. フォルダの削除 ---
print("\n--- 8. フォルダの削除 ---")
# os.rmdir(パス) は、空のフォルダしか削除できません。
# フォルダ内にファイルなどがある場合はエラーになります。
# 中身があるフォルダを削除するには、shutil.rmtree() を使いますが、これは注意が必要です。
if os.path.exists(folder_name) and not list(os.listdir(folder_name)): # フォルダが空であることを確認
    os.rmdir(folder_name)
    print(f"フォルダ '{folder_name}' を削除しました。")
elif os.path.exists(folder_name):
    print(f"フォルダ '{folder_name}' は空ではないため、os.rmdir()では削除できませんでした。")