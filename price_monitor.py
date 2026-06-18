from bs4 import BeautifulSoup
import requests
import re

def get_current_price():

    url = "https://www.ctfmall.com/goods?mouldNo=F235926"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    soup = BeautifulSoup(resp.text, "html.parser")

    price_div = soup.select_one(".price-show")

    if price_div:

        text = price_div.get_text(" ", strip=True)

        print("price-show内容:")
        print(text)

        match = re.search(
            r"([0-9,]+\.[0-9]{2})",
            text
        )

        if match:
            price = float(
                match.group(1).replace(",", "")
            )

            print("解析价格:", price)

            return price

    print("未找到价格")

    return None
