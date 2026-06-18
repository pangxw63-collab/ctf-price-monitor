import os
import re
import requests
from datetime import datetime

PRODUCT_CODE = "F235926"

URL = f"https://www.ctfmall.com/goods?mouldNo={PRODUCT_CODE}"

def get_current_price():

```
headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(
    URL,
    headers=headers,
    timeout=30
)

print("========== 页面调试 ==========")
print("状态码:", resp.status_code)
print("最终URL:", resp.url)

html = resp.text

print("页面长度:", len(html))
print("前2000字符:")
print(html[:2000])

print("========== 查找价格 ==========")

matches = re.findall(
    r"[0-9]{4,6}\.[0-9]{2}",
    html
)

print("发现数字:")
print(matches[:20])

print("=============================")

return "调试模式"
```

def send_feishu(message):

```
webhook = os.getenv("FEISHU_WEBHOOK")

print("========== FEISHU DEBUG ==========")

if webhook:
    print("Webhook已读取")
    print("长度:", len(webhook))
else:
    print("Webhook未读取")

print("=================================")

if not webhook:
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
```

def main():

```
price = get_current_price()

msg = f"""
```

【周大福价格监控】

商品型号: {PRODUCT_CODE}

当前价格:
{price}

检查时间:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

```
print(msg)

send_feishu(msg)
```

if **name** == "**main**":
main()
