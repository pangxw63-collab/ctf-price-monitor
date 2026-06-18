import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

PRODUCT_CODE = "F235926"

URL = f"https://www.ctfmall.com/goods?mouldNo={PRODUCT_CODE}"


from playwright.sync_api import sync_playwright



def get_current_price():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        price_text = page.locator(
            ".price-show"
        ).inner_text()

        print("price-show:")
        print(price_text)

        browser.close()

    text = (
        price_text
        .replace("¥", "")
        .replace("起", "")
        .replace(",", "")
        .strip()
    )

    match = re.search(
        r"(\d+\.\d+)",
        text
    )

    if not match:
        return None

    return float(match.group(1))


def send_feishu(message):

    webhook = os.getenv("FEISHU_WEBHOOK")

    if not webhook:
        print("未配置 FEISHU_WEBHOOK")
        return

    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    resp = requests.post(
        webhook,
        json=data,
        timeout=20
    )

    print("飞书状态码:", resp.status_code)
    print("飞书返回:", resp.text)


def main():

    price = get_current_price()

    if price is None:
        price_text = "获取失败"
    else:
        price_text = f"¥{price:,.2f}"

    msg = f"""
【周大福价格监控】

商品型号: {PRODUCT_CODE}

当前价格:
{price_text}

商品链接:
{URL}

检查时间:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    print(msg)

    send_feishu(msg)


if __name__ == "__main__":
    main()
