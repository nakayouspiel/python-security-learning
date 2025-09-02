import pystray
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import decimal
import time
import threading
from threading import Event
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import os
import sys

# Windows OSのスリープイベントを扱うためのライブラリをインポート
try:
    from win32api import GetSystemMetrics, SetSystemPowerState
    from win32con import PBT_APMRESUMESUSPEND
    import win32gui
    import win32con
except ImportError:
    print("Pywin32ライブラリが見つかりませんでした。pip install pywin32を実行してください。")
    # 代替処理（win32apiがない場合の動作）
    pass

# Googleスプレッドシート連携のためのライブラリをインポート
import gspread
from google.oauth2 import service_account

# 表示モードを管理するグローバル変数
# 0: 小数点以下2,3桁, 1: 小数点以下1,2桁, 2: 現在値（銭）
display_mode = 0

# 選択された通貨を管理するグローバル変数
selected_currency = "TRY_JPY"

# 日付が変わるたびに、その日の最初の価格が自動的にここに設定されます。
previous_day_baseline = decimal.Decimal('0')

# 最後に基準値を更新した日付を保存する箱
last_update_date = None

# メニューから呼び出す関数を定義
def set_display_mode(icon, item):
    global display_mode
    mode = ["Difference (Cents)", "Difference (Yen)", "Current Price"].index(item.text)
    display_mode = mode

def set_currency(icon, item):
    global selected_currency
    global previous_day_baseline
    
    if item.text == "TRY/JPY":
        selected_currency = "TRY_JPY"
    elif item.text == "USD/JPY":
        selected_currency = "USD_JPY"
    
    previous_day_baseline = decimal.Decimal('0')
    get_initial_baseline_from_gsheet()

# 手動入力を置き換え、Googleスプレッドシートから基準値を取得する関数
def get_initial_baseline_from_gsheet():
    global previous_day_baseline
    
    # スプレッドシートを認証するための設定
    try:
        # PyInstallerで実行されているかを確認し、ファイルのパスを適切に設定する
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstallerで実行されている場合
            base_path = sys._MEIPASS
        else:
            # スクリプトとして直接実行されている場合
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        credentials_path = os.path.join(base_path, 'currency-monitor-tool-7e3d63d0ebf0.json')

        creds = service_account.Credentials.from_service_account_file(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        gc = gspread.authorize(creds)
        
        # 'currency-monitor-data'をあなたのスプレッドシートの名前に書き換えてください
        sh = gc.open('currency-monitor-data')
        worksheet = sh.worksheet("シート1") # 1つ目のシートを取得
        
        # 選択された通貨に応じてセルから値を取得
        if selected_currency == "TRY_JPY":
            cell_to_get = 'B2'
        elif selected_currency == "USD_JPY":
            cell_to_get = 'B4'
        
        yesterday_close = worksheet.acell(cell_to_get).value
        
        if yesterday_close:
            previous_day_baseline = decimal.Decimal(yesterday_close).quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
            print(f"基準価格をGoogleスプレッドシートから {previous_day_baseline} に設定しました。")
        else:
            print("Googleスプレッドシートから終値を取得できませんでした。")
    except Exception as e:
        print(f"Googleスプレッドシートからのデータ取得に失敗しました: {e}")
        print("基準価格は自動で設定されます。")

# スリープ復帰を検知するウィンドウクラスを作成
class SleepResumeDetector:
    def __init__(self):
        # ウィンドウクラスの登録
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wndProc
        wc.lpszClassName = "SleepResumeDetectorClass"
        self.classAtom = win32gui.RegisterClass(wc)
        
        # 非表示ウィンドウの作成
        self.hwnd = win32gui.CreateWindow(
            self.classAtom,
            "SleepResumeDetector",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            win32gui.GetModuleHandle(None),
            None
        )
        print("スリープ検知ウィンドウを作成しました。")

    def wndProc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_POWERBROADCAST:
            if wparam == PBT_APMRESUMESUSPEND:
                # スリープから復帰したことを検出
                print("スリープからの復帰を検出しました。レート更新を再開します。")
                # ここで更新処理のフラグを立てるか、直接更新処理を呼び出す
                update_rate_on_resume.set()
        return 0

# スリープ復帰時に更新を再開するためのイベント
update_rate_on_resume = Event()

# 為替レート取得と更新処理を行う関数
def update_rate(icon, stop_event):
    global previous_day_baseline
    global display_mode
    global last_update_date
    global selected_currency

    API_ENDPOINT = "https://forex-api.coin.z.com/public"
    PATH = "/v1/ticker"
    
    while not stop_event.is_set():
        try:
            # スリープ復帰イベントが発生するまで待機する
            if update_rate_on_resume.is_set():
                update_rate_on_resume.clear()
            
            response = requests.get(API_ENDPOINT + PATH)
            
            api_data = response.json()
            if api_data["status"] == 0:
                all_tickers = api_data["data"]
                
                selected_info = None
                for ticker in all_tickers:
                    if ticker["symbol"] == selected_currency:
                        selected_info = ticker
                        break
                
                if selected_info:
                    current_date_str = selected_info["timestamp"].split('T')[0]
                    current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
                    
                    if last_update_date is None:
                        last_update_date = current_date
                    
                    if last_update_date != current_date:
                        last_update_date = current_date
                        previous_day_baseline = decimal.Decimal('0')
                    
                    bid_price_decimal = decimal.Decimal(selected_info["bid"])
                    
                    if previous_day_baseline == decimal.Decimal('0'):
                        previous_day_baseline = bid_price_decimal.quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)

                    main_digits = ""
                    difference = decimal.Decimal('0')

                    fill_color = (0, 0, 0)
                    if difference > 0:
                        fill_color = (255, 0, 0)
                    elif difference < 0:
                        fill_color = (0, 0, 255)
                    
                    if display_mode == 2:
                        rounded_price = bid_price_decimal.quantize(decimal.Decimal('0.1'), rounding=decimal.ROUND_HALF_UP)
                        main_digits = str(int(rounded_price * 10))
                        fill_color = (0, 0, 0)
                    
                    else: # display_modeが0か1の場合
                        difference = bid_price_decimal - previous_day_baseline
                        
                        # 色の判定を先に行う
                        fill_color = (0, 0, 0)
                        if difference > 0:
                            fill_color = (255, 0, 0) # 赤
                        elif difference < 0:
                            fill_color = (0, 0, 255) # 青
                        
                        # 判定後、表示用の文字列を作成
                        if display_mode == 0:
                            rounded_diff = abs(difference).quantize(decimal.Decimal('0.001'), rounding=decimal.ROUND_HALF_UP)
                            main_digits = str(int(rounded_diff * 1000))
                        elif display_mode == 1:
                            rounded_diff = abs(difference).quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
                            main_digits = str(int(rounded_diff * 100))
                        
                        if main_digits == "0":
                            main_digits = "0"
                            difference = decimal.Decimal('0')

                        icon.icon = create_image(main_digits, fill_color)        
                        
                        
                    
                    icon.icon = create_image(main_digits, fill_color)
                else:
                    icon.icon = create_image("ERR")
            else:
                icon.icon = create_image("ERR")

        except requests.exceptions.RequestException:
            icon.icon = create_image("NET")
        except (json.JSONDecodeError, KeyError):
            icon.icon = create_image("ERR")

        time.sleep(5)

# アイコンを作成する関数
def create_image(text, fill_color=(0, 0, 0)):
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    
    if text in ["ERR", "NET"]:
        try:
            error_font = ImageFont.truetype("arial.ttf", 25)
            dc.text((32, 32), text, font=error_font, fill=fill_color, anchor='mm')
        except IOError:
            error_font = ImageFont.load_default()
            dc.text((32, 32), text, font=error_font, fill=fill_color, anchor='mm')
    else:
        try:
            main_font = ImageFont.truetype("arial.ttf", 60)
            dc.text((32, 32), text, font=main_font, fill=fill_color, anchor='mm')
        except IOError:
            main_font = ImageFont.load_default()
            dc.text((32, 32), text, font=fill_color, anchor='mm')
    
    return image

# 終了処理用の関数
def on_quit(icon, stop_event):
    stop_event.set()
    icon.stop()

# アイコンの作成と実行
if __name__ == '__main__':
    get_initial_baseline_from_gsheet()

    icon_image = create_image("0")
    stop_event = Event()
    
    # スリープ復帰検知のためのスレッドとウィンドウを作成
    try:
        sleep_detector = SleepResumeDetector()
    except:
        print("Pywin32が利用できないため、スリープ復帰検知機能は無効です。")
    
    menu = pystray.Menu(
        pystray.MenuItem(
            "Display Mode",
            pystray.Menu(
                pystray.MenuItem("Difference (Cents)", lambda icon, item: set_display_mode(icon, item), checked=lambda item: display_mode == 0),
                pystray.MenuItem("Difference (Yen)", lambda icon, item: set_display_mode(icon, item), checked=lambda item: display_mode == 1),
                pystray.MenuItem("Current Price", lambda icon, item: set_display_mode(icon, item), checked=lambda item: display_mode == 2)
            )
        ),
        pystray.MenuItem(
            "Currency",
            pystray.Menu(
                pystray.MenuItem("TRY/JPY", lambda icon, item: set_currency(icon, item), checked=lambda item: selected_currency == "TRY_JPY"),
                pystray.MenuItem("USD/JPY", lambda icon, item: set_currency(icon, item), checked=lambda item: selected_currency == "USD_JPY")
            )
        ),
        pystray.MenuItem('Exit', lambda icon: on_quit(icon, stop_event))
    )
    
    icon = pystray.Icon("exchange_rate_tray", icon_image, "currency", menu)
    
    thread = threading.Thread(target=update_rate, args=(icon, stop_event))
    thread.daemon = True
    thread.start()
    
    icon.run()