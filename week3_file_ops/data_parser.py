import csv
import re # 正規表現モジュール
from pathlib import Path

# --- CSVファイルの読み込み ---
print("--- CSVファイルの読み込み ---")
csv_file_path = Path("sample.csv") # スクリプトと同じフォルダにあるCSVファイル

if csv_file_path.exists():
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file) # csv.readerオブジェクトを作成
        header = next(reader) # ヘッダー行を読み込む (例: ['id', 'name', 'age', 'city'])
        print(f"ヘッダー: {header}")

        data = []
        for row in reader: # ヘッダーの次の行から、各行をリストとして読み込む
            data.append(row)
            print(f"データ行: {row}")

    print("\nCSVデータ全体:")
    for row_data in data:
        print(row_data)

    # 例：特定の条件でデータを抽出 (ageが30以上の人)
    print("\n--- 年齢が30歳以上のユーザー ---")
    for row_data in data:
        try:
            # CSVから読み込んだデータは全て文字列なので、int()で数値に変換して比較
            # row_data[2] はリストの3番目の要素（インデックス2）で、'age' の値です
            if int(row_data[2]) >= 30:
                print(f"名前: {row_data[1]}, 年齢: {row_data[2]}")
        except ValueError:
            # ageが数値に変換できない場合の例外処理（例：データが破損している、空行など）
            print(f"エラー: 年齢が無効な行をスキップしました - {row_data}")
        except IndexError:
            # 行の要素数が不足している場合の例外処理
            print(f"エラー: 要素が不足している行をスキップしました - {row_data}")
else:
    print(f"CSVファイル '{csv_file_path}' が見つかりませんでした。")


# --- テキストログからの情報抽出（正規表現の初歩） ---
print("\n--- テキストログからの情報抽出 ---")
log_file_path = Path("app_log.txt") # スクリプトと同じフォルダにあるログファイル

if log_file_path.exists():
    with open(log_file_path, 'r', encoding='utf-8') as file:
        log_content = file.read() # ログファイル全体を一つの大きな文字列として読み込む

    # 例1: ERRORの行を抽出
    print("\n--- ERRORログ ---")
    # re.findall(パターン, 文字列) は、パターンに一致する部分を全て見つけてリストで返します。
    # r"..." は「raw string（生文字列）」で、\（バックスラッシュ）をエスケープしないことを意味します。正規表現では\を頻繁に使うため、r"..."形式が推奨されます。
    # .*? は、任意の文字が0回以上繰り返すことを意味します。（? は最短一致）
    # () は「キャプチャグループ」で、括弧の中の内容を抽出したい場合に指定します。
    error_pattern = r"\[(.*?)\] ERROR: (.*)" # 例: [2025-07-31 10:00:15] ERROR: Database connection failed. Retrying...
    errors = re.findall(error_pattern, log_content) # [(日付 時間, エラーメッセージ), ...] のリストになる
    for timestamp, message in errors:
        print(f"時刻: {timestamp}, エラー: {message}")

    # 例2: ログインユーザーとIPアドレスを抽出
    print("\n--- ログイン情報 ---")
    login_pattern = r"User '(.*?)' logged in from (.*)." # 例: User 'Alice' logged in from 192.168.1.10.
    logins = re.findall(login_pattern, log_content) # [(ユーザー名, IPアドレス), ...] のリストになる
    for username, ip_address in logins:
        print(f"ユーザー: {username}, IPアドレス: {ip_address}")

    # 例3: 不正アクセスIPアドレスを抽出
    print("\n--- 不正アクセス試行 ---")
    unauthorized_pattern = r"Unauthorized access attempt from (.*?)." # 例: Unauthorized access attempt from 203.0.113.4.
    unauthorized_ips = re.findall(unauthorized_pattern, log_content) # [IPアドレス, ...] のリストになる
    for ip in unauthorized_ips:
        print(f"不正アクセス元IP: {ip}")

else:
    print(f"ログファイル '{log_file_path}' が見つかりませんでした。")

print("\n--- データ解析が完了しました ---")