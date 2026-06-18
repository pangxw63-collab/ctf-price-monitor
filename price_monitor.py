import os
import json
from datetime import datetime

# TODO:
# 1. 找到周大福商品接口或网页链接
# 2. 在 get_current_price() 中实现实际抓取逻辑

PRODUCT_CODE = "F234661"

def get_current_price():
    # 示例价格，请替换为真实抓取逻辑
    return 13336.62

def main():
    price = get_current_price()

    history_file = "price_history.json"

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    last_price = history[-1]["price"] if history else None

    history.append({
        "time": datetime.now().isoformat(),
        "price": price
    })

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"商品 {PRODUCT_CODE}")
    print(f"当前价格: ¥{price}")

    if last_price is not None:
        diff = round(price - last_price, 2)
        print(f"较上次变化: {diff:+.2f}")

if __name__ == "__main__":
    main()
