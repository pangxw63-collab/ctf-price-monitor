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

    print("========== 请求页面 ==========")

    resp = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    print("状态码:", resp.status_code)
    print("最终URL:", resp.url)

    html = resp.text

    print("页面长度:", len(html))

    print("========== HTML前500字符 ==========")
    print(html[:500])

    print("=================================")

    print(
        "是否存在price-show:",
        "price-show" in html
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    price_div = soup.select_one(
        ".price-show"
    )

    if price_div:

        text = price_div.get_text(
            " ",
            strip=True
        )

        print("price-show内容:")
        print(text)

        match = re.search(
            r"([0-9,]+\.[0-9]{2})",
            text
        )

        if match:

            price = float(
                match.group(1)
                .replace(",", "")
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

商品型号: {PRODUCT_CODE}

当前价格:
{price}

检查时间:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    print(msg)

    send_feishu(msg)


if __name__ == "__main__":
    main()
