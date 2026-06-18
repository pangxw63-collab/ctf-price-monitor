import requests
import os

# 商品参数
WEIGHT = 19.23
LABOR_FEE = 620

# 飞书机器人Webhook
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK")


def get_gold_price():
    url = "https://push2.eastmoney.com/api/qt/stock/get"

    params = {
        "secid": "113.AU9999",
        "fields": "f43"
    }

    r = requests.get(url, params=params, timeout=20)

    data = r.json()

    price = data["data"]["f43"] / 100

    return price

print(get_gold_price())


def send_feishu(text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    requests.post(
        FEISHU_WEBHOOK,
        json=data,
        timeout=20
    )


def main():

    gold_price = get_gold_price()

    sale_price = gold_price * WEIGHT + LABOR_FEE

    msg = f"""
【黄金价格监控】

实时金价：{gold_price:.2f} 元/克

商品克重：{WEIGHT} g
工费：{LABOR_FEE} 元

预计售价：
{sale_price:.2f} 元
"""

    print(msg)

    send_feishu(msg)


if __name__ == "__main__":
    main()
