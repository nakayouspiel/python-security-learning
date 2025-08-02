import socket
import sys

# 1. スキャン対象のホストとポート範囲を指定
# HOSTに指定したドメイン名やIPアドレスのポートをスキャンします。
# ここでは、セキュリティの懸念がないローカルPC（localhost）を対象にします。
HOST = '127.0.0.1'  # ローカルPCを示すIPアドレス
PORT_RANGE = range(136, 138)  # スキャンするポートの範囲（1から1024まで）
TIMEOUT = 1  # タイムアウト時間（秒）

print(f"--- ポートスキャンを開始します: {HOST} ---")
print(f"スキャンするポート範囲: {PORT_RANGE.start} から {PORT_RANGE.stop - 1} まで")

# 2. ポートを一つずつチェック
for port in PORT_RANGE:
    # socket.AF_INET はIPv4、socket.SOCK_STREAM はTCPプロトコル
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)  # タイムアウトを設定

    try:
        # 接続を試みる
        s.connect((HOST, port))
        print(f"[+] Port {port} is OPEN")
    except socket.timeout:  
        # タイムアウトした場合
        # print(f"[-] Port {port} is CLOSED (Timeout)") # デバッグ用にコメント解除
        pass  # 何もしない
    except ConnectionRefusedError:
        # 接続が拒否された場合
        # print(f"[-] Port {port} is CLOSED (Refused)") # デバッグ用にコメント解除
        pass  # 何もしない
    except PermissionError: # <-- この行を追加！
        print(f"[-] Port {port} is FILTERED (Permission denied)")
    except Exception as e:
        # その他のエラー
        print(f"[*] Port {port} has an error: {e}")

    s.close()  # ソケットを閉じる

print("--- ポートスキャンが完了しました ---")