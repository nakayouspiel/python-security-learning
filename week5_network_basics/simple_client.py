import socket

# 接続先のホスト（IPアドレスまたはドメイン名）とポート番号
# この例では、Echo Protocol (エコープロトコル) のテストサーバーに接続します。
# Echoサーバーは、送られてきたデータをそのまま返します。
HOST = 'google.com' # テスト用Echoサーバー
PORT = 80  # Echoプロトコルの標準ポート番号

# 1. ソケットの作成
# socket.AF_INET はIPv4を使用することを示します。
# socket.SOCK_STREAM はTCPプロトコルを使用することを示します。
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 2. サーバーへの接続
    print(f"Connecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    print("Connected.")

    # 3. データの送信
    message = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
    # 文字列はそのままでは送信できないので、バイト列にエンコードします。
    s.sendall(message.encode('ascii'))
    print(f"Sent: Http request to {HOST}")

     # 4. データを受信
    # 1024は受信するデータの最大バイト数です。
    data = s.recv(1024)
    # 受信したバイト列を文字列にデコード
    received_data = data.decode('ascii', errors='ignore')
    print(f"Received data from {HOST}:")
    print("---")
    print(received_data)
    print("---")

print("\n--- クライアント処理が完了しました ---")