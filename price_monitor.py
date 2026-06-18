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

    print("状态码:", resp.status_code)
    print("HTML长度:", len(resp.text))

    print(
        "price-show存在:",
        "price-show" in resp.text
    )

    print("HTML前1000字符:")
    print(resp.text[:1000])

    soup = BeautifulSoup(
        resp.text,
        "html.parser"
    )

    price_div = soup.select_one(".price-show")

    if not price_div:
        print("未找到 .price-show")
        return None

    text = price_div.get_text(
        "",
        strip=True
    )

    print("price-show内容:")
    print(text)

    text = (
        text.replace("¥", "")
            .replace("起", "")
            .replace(",", "")
            .strip()
    )

    match = re.search(
        r"(\d+\.\d+)",
        text
    )

    if not match:
        print("价格解析失败")
        return None

    price = float(match.group(1))

    print("解析价格:", price)

    return price


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
