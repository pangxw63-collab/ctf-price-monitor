import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCT_CODE = "F235926"

URL = f"https://www.ctfmall.com/goods?mouldNo={PRODUCT_CODE}"


def get_current_price():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    soup = BeautifulSoup(
        resp.text,
        "html.parser"
    )

    price_div = soup.select_one(
        ".price-show"
    )

    if not price_div:
        print("未找到 price-show")
        return None

    text = price_div.get_text(
        "",
        strip=True
    )

    print("price-show原始内容:")
    print(text)

    text = (
        text
        .replace("¥", "")
        .replace("起", "")
        .replace(",", "")
        .strip()
    )

    print("清洗后:")
    print(text)

    match = re.search(
        r"(\d+\.\d+)",
        text
    )

    if not match:
        print("价格解析失败")
        return None

    price = float(
        match.group(1)
    )

    print("解析价格:", price)

    return price

    print("未找到价格")

    return None


def send_feishu(message):

    webhook = os.getenv(
        "FEISHU_WEBHOOK"
    )

    print("========== FEISHU ==========")

    if webhook:

        print("Webhook存在")
        print("Webhook长度:", len(webhook))

    else:

        print("Webhook不存在")
        return

    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    try:

        resp = requests.post(
            webhook,
            json=data,
            timeout=20
        )

        print(
            "飞书状态码:",
            resp.status_code
        )

        print(
            "飞书返回:",
            resp.text
        )

    except Exception as e:

        print(
            "飞书发送异常:",
            str(e)
        )


def main():

    price = get_current_price()

msg = f"""
【周大福价格监控】

型号: {PRODUCT_CODE}

当前售价:
¥{price:,.2f}

商品链接:
{URL}

时间:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    print(msg)

    send_feishu(msg)


if __name__ == "__main__":
    main()
