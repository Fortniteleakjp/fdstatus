import requests
import time
import json
from discordrp import Presence
import warnings
import hashlib
import logging  #ログの保存用ライブラリを追加

warnings.filterwarnings("ignore", category=ResourceWarning)

#ログの設定
logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

GREEN = "\033[32m"  #緑色
YELLOW = "\033[33m"  #黄色
RED = "\033[31m"  #赤色
RESET = "\033[0m"  #色リセット
IMAGE_KEY = "image"
ACCOUNT_TYPE = "epic"
TIME_WINDOW = "lifetime"
API_URL = f"https://fortnite-api.com/v2/stats/br/v2"
GITHUB_URL = "https://github.com/Fortniteleakjp/fortnitediscordstatus"

APPNAME = "フォートナイト統計"

#githubへのリンク用のはっしゅさくせい
def generate_match_hash():
    return hashlib.md5(GITHUB_URL.encode()).hexdigest()

#ユーザー設定をJSONファイルに保存
def save_settings_to_json(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats):
    settings = {
        "DISCORD_APP_ID": DISCORD_APP_ID,
        "FORTNITE_API_KEY": FORTNITE_API_KEY,
        "ACCOUNT_NAME": ACCOUNT_NAME,
        "SELECTED_STATS": selected_stats  #ユーザーが選択した統計も保存
    }
    try:
        with open('settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(settings, json_file, ensure_ascii=False, indent=4)
        logging.info(f"設定がsettings.jsonに保存されました: {selected_stats}")
    except Exception as e:
        logging.error(f"設定ファイル保存エラー: {e}")

def log_user_input(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats):
    try:
        logging.info(f"DiscordアプリケーションID: {DISCORD_APP_ID}")
        logging.info(f"APIキー: {FORTNITE_API_KEY}")
        logging.info(f"Fortniteアカウント名: {ACCOUNT_NAME}")
        logging.info(f"選択された統計: {', '.join(selected_stats)}")
    except Exception as e:
        logging.error(f"ユーザー入力ログ記録エラー: {e}")

#設定をJSONファイルから読み込む
def load_settings_from_json():
    try:
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            settings = json.load(json_file)
        return settings
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"設定ファイル読み込みエラー: {e}")
        return None

#APIからデータを取得
def get_fortnite_stats(api_key, account_name):
    headers = {"Authorization": api_key}
    params = {
        "name": account_name,
        "accountType": ACCOUNT_TYPE,
        "timeWindow": TIME_WINDOW,
    }
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        with open('fortnite_stats.json', 'w', encoding='utf-8') as json_file:
            json.dump(response.json(), json_file, ensure_ascii=False, indent=4)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"APIリクエストエラー: {e}")
        print(f"{RED}APIリクエストでエラーが発生しました{RESET}")
        print(f"{RED}APIkeyやアカウント名が正しいか確認してください")
        return None
    except Exception as e:
        logging.error(f"APIデータ取得エラー: {e}")
        print(f"{RED}データ取得中にエラーが発生しました{RESET}")
        return None

def get_user_stat_choices():
    print(f"{YELLOW}表示する統計を選んでください（最大2つまで選択可能）{RESET}")
    print("1: 総キル数")
    print("2: 総マッチ数")
    print("3: ビクロイ数")
    print("4: 勝率")
    print("5: 平均キル数")
    selected_stats = []
    while len(selected_stats) < 2:
        choice = input(f"{GREEN}選択肢を入力してください (1-5) または '終了' と入力で終了: {RESET}")
        if choice == '終了':
            break
        if choice in ['1', '2', '3', '4', '5'] and choice not in selected_stats:
            selected_stats.append(choice)
        else:
            print(f"{RED}無効な選択肢です。再度入力してください。{RESET}")
    return selected_stats

def update_discord_presence(stats, presence, start_time, remaining_time, selected_stats):
    try:
        overall_stats = stats['data']['stats']['all']['overall']
        wins = overall_stats['wins']
        kills = overall_stats['kills']
        matches = overall_stats['matches']
        win_rate = (wins / matches) * 100 if matches > 0 else 0
        average_kills = kills / matches if matches > 0 else 0

        state = APPNAME
        #ユーザーの選択に基づいてdetailsを作成
        details = ""
        if '1' in selected_stats:
            details += f"総キル数: {kills} | "
        if '2' in selected_stats:
            details += f"総マッチ数: {matches} | "
        if '3' in selected_stats:
            details += f"ビクロイ数: {wins} | "
        if '4' in selected_stats:
            details += f"勝率: {win_rate:.2f}% | "
        if '5' in selected_stats:
            details += f"平均キル数: {average_kills:.2f}"
        if details.endswith(' | '):
            details = details[:-3]

        match_hash = generate_match_hash()

        presence.set({
            "state": state,
            "details": details,
            "timestamps": {
                "start": start_time,
                "end": start_time + remaining_time
            },
            "assets": {
                "large_image": IMAGE_KEY,
            },
            "match": match_hash,
            "instance": True,
        })
        print(f"{YELLOW}統計データをDiscordに表示しました{RESET}")
    except Exception as e:
        logging.error(f"Discordステータス更新エラー: {e}")
        print(f"{RED}Discordのステータス更新中にエラーが発生しました: {e}{RESET}")

#メイン処理
def main():
    try:
        settings = load_settings_from_json()

        if settings:
            #設定が存在する場合、「設定ファイルから自動で読み込みますか？」と確認
            print(f"{YELLOW}設定ファイルが見つかりました。設定を自動で読み込みますか？ (y/n){RESET}", end="")
            choice = input().strip().lower()

            if choice == 'y':
                #「y」が選ばれたら自動で読み込み
                print(f"{YELLOW}設定が読み込まれました{RESET}")
                print(f"{GREEN}アカウント名: {settings['ACCOUNT_NAME']}")
                DISCORD_APP_ID = settings['DISCORD_APP_ID']
                FORTNITE_API_KEY = settings['FORTNITE_API_KEY']
                ACCOUNT_NAME = settings['ACCOUNT_NAME']
                selected_stats = settings['SELECTED_STATS']  #設定ファイルから選択された統計をロード
            elif choice == 'n':
                #「n」が選ばれたら新たに入力
                print(f"{YELLOW}新たに設定を入力してください。{RESET}")
                print(f"{GREEN}DiscordアプリケーションIDを入力してください: {RESET}", end="")
                DISCORD_APP_ID = input()
                print(f"{GREEN}APIキーを入力してください: {RESET}", end="")
                FORTNITE_API_KEY = input()
                print(f"{GREEN}アカウント名を入力してください: {RESET}", end="")
                ACCOUNT_NAME = input()

                #ユーザー設定を保存
                selected_stats = get_user_stat_choices()
                save_settings_to_json(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats)
                log_user_input(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats)
                print(f"{YELLOW}設定が保存されました{RESET}")
            else:
                print(f"{RED}無効な選択です。終了します。{RESET}")
                return
        else:
            print(f"{YELLOW}設定ファイルが見つかりませんでした。新たに入力してください。{RESET}")
            DISCORD_APP_ID = input(f"{GREEN}DiscordアプリケーションIDを入力してください: {RESET}")
            FORTNITE_API_KEY = input(f"{GREEN}APIキーを入力してください: {RESET}")
            ACCOUNT_NAME = input(f"{GREEN}アカウント名を入力してください: {RESET}")
            selected_stats = get_user_stat_choices()

            #ユーザー設定を保存
            save_settings_to_json(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats)
            log_user_input(DISCORD_APP_ID, FORTNITE_API_KEY, ACCOUNT_NAME, selected_stats)
            print(f"{YELLOW}設定が保存されました{RESET}")

        #データの更新間隔は60秒に固定
        UPDATE_INTERVAL = 60
        print(f"{YELLOW}データは{UPDATE_INTERVAL}秒ごとに更新されます{RESET}")

        print(f"{YELLOW}統計データを取得中...{RESET}")
        stats = get_fortnite_stats(FORTNITE_API_KEY, ACCOUNT_NAME)
        if not stats:
            print(f"{RED}統計データの取得に失敗しました。{RESET}")
            return

        with Presence(DISCORD_APP_ID) as presence:
            print(f"{GREEN}Discordに接続しました{RESET}")
            start_time = int(time.time())
            remaining_time = UPDATE_INTERVAL
            update_discord_presence(stats, presence, start_time, remaining_time, selected_stats)
            try:
                while True:
                    time.sleep(UPDATE_INTERVAL)
                    stats = get_fortnite_stats(FORTNITE_API_KEY, ACCOUNT_NAME)
                    if stats:
                        start_time = int(time.time())
                        update_discord_presence(stats, presence, start_time, remaining_time, selected_stats)
            except KeyboardInterrupt:
                print(f"{RED}終了します。{RESET}")

    except Exception as e:
        logging.error(f"メイン処理エラー: {e}")
        print(f"{RED}プログラム実行中にエラーが発生しました: {e}{RESET}")

if __name__ == "__main__":
    main()