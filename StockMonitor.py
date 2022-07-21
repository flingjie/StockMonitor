import json
import requests
import schedule
import time

def send_to_feishu(content):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/3c6d60b8-xxx" # 这里是实际的webhook地址
    msg = {"msg_type": "text", "content": {"text": content}} # 这里发送文本内容即可
    res = requests.post(url, json=msg)
    print(res.json()) 
    
# 获取股票实时价格
def get_price(code):  
    url = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={code},m1,,10'
    print(url)
    stock_name = ""
    resp = requests.get(url).json()
    if resp['code'] != 0:
        return stock_name, []
    stock_name = resp['data'][code]['qt'][code][1]
    latest_prices = resp['data'][code]["m1"][-1]
    return stock_name, latest_prices


# 循环监控
def monitor():
    stocks = [
        {
        "code": "sh688068",
        "min": 230,
        "max": 239
    },
    {
        "code": "sh000001",
        "min": 3530,
        "max": 3550
    }]
    for c in stocks:
        print(f'check => {c["code"]}')
        # 获取股票最新价格, 返回列表依次为'day', 'open', 'high', 'low', 'close', 'volume'
        stock_name, prices = get_price(c["code"])

        print(prices)
        if not prices:
            continue

        if float(prices[3]) < c["min"]:
            content = f'{stock_name}({c["code"]})当前价格:{prices[3]}<最低价({c["min"]})'
            send_to_feishu(content)
        if float(prices[2]) > c['max']:
            content = f'{stock_name}({c["code"]})当前价格:{prices[2]}>监控价({c["max"]})'
            send_to_feishu(content)
            
schedule.every(5).minutes.do(monitor)
while True:
    schedule.run_pending()
    time.sleep(1)
