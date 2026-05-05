import requests
import time
import random
import hashlib
from datetime import datetime

def log(msg):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

# 監視URL
url = "https://hotel.travel.rakuten.co.jp/hotelinfo/plan/140784?f_flg=PLAN&f_teikei=&f_hizuke=&f_hak=&f_dai=japan&f_chu=ehime&f_shou=chuuyo&f_sai=&f_tel=&f_target_flg=&f_tscm_flg=&f_p_no=&f_custom_code=&f_search_type=&f_camp_id=&f_static=1&f_squeezes=kinen&f_rm_bed=twin&f_rm_equip=&f_hi1=5&f_tuki1=5&f_nen1=2026&f_hi2=6&f_tuki2=5&f_nen2=2026&f_heya_su=2&f_otona_su=4&f_s1=0&f_s2=0&f_y1=0&f_y2=0&f_y3=0&f_y4=0&f_kin2=0&f_kin="

# ntfy通知先
notify_url = "https://ntfy.sh/akira-hotel-watch"

headers = {
    "User-Agent": "Mozilla/5.0"
}

last_hash = None

log("楽天トラベル監視スタート")

##### while True:

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        # HTMLの変化検出
        current_hash = hashlib.md5(html.encode("utf-8")).hexdigest()

        if last_hash and last_hash != current_hash:
            log("ページ内容が変化しました")

        last_hash = current_hash

        # 空室判定
        if "ご指定の条件での空室が見つかりませんでした" not in html:

            log("空室の可能性あり！")

            message = f"""
楽天ホテル 空室の可能性あり！

{url}

{datetime.now()}
"""

            requests.post(
                notify_url,
                data=message.encode("utf-8")
            )

            log("通知送信")
            break

        else:
            message = f"""
楽天ホテル 空きなし

{url}

{datetime.now()}
"""

            requests.post(
                notify_url,
                data=message.encode("utf-8")
            )

            log("空きなし")

        # ログ保存
        with open("rakuten_watch.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} チェック\n")

    except Exception as e:
        log("通信エラー:", e)

        message = f"""
楽天監視エラー

{e}

{datetime.now()}
"""

        requests.post(
            notify_url,
            data=message.encode("utf-8")
        )

    # ランダム監視
    wait = random.randint(40,90)
    print(f"{wait}秒待機")
    time.sleep(wait)
