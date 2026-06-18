import os
import requests
from datetime import datetime

PRODUCT_CODE = "F234661"


def get_current_price():
    """
    临时测试价格
    后面替换成周大福真实抓取逻辑
    """
    return 13336.62


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

    print("飞书返回状态:", resp.status_code)
    print("飞书返回内容:", resp.text)


def main():
    price = get_current_price()

    message = f"""
【周大福价格监控】

商品型号：{PRODUCT_CODE}

当前价格：¥{price}

检查时间：
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    print(message)

    send_feishu(message)


if __name__ == "__main__":
    main()
