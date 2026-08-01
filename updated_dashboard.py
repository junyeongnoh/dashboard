import yfinance as yf
import requests
import re
from datetime import datetime
import os

def get_rates():
    print("금리 수집 중...")
    y2 = round(yf.Ticker("^IRX").fast_info["lastPrice"], 2)
    y5 = round(yf.Ticker("^FVX").fast_info["lastPrice"], 2)
    y10 = round(yf.Ticker("^TNX").fast_info["lastPrice"], 2)
    print(f"  2년물:{y2}  5년물:{y5}  10년물:{y10}")
    return y2, y5, y10

def get_fx():
    print("환율 수집 중...")
    fx = int(round(yf.Ticker("USDKRW=X").fast_info["lastPrice"], 0))
    print(f"  USD/KRW:{fx}")
    return fx

def get_tga():
    print("TGA 수집 중...")
    url = (
        "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
        "/v1/accounting/dts/operating_cash_balance"
        "?filter=account_type:eq:Federal%20Reserve%20Account"
        "&sort=-record_date&page[size]=1&format=json"
    )
    data = requests.get(url, timeout=10).json()
    tga = round(float(data["data"][0]["open_today_bal"]) / 1000, 1)
    print(f"  TGA:{tga}B$")
    return tga

def add_value(html, key, value, is_str=False):
    if value is None:
        return html
    v = '"' + str(value) + '"' if is_str else str(value)
    pattern = '(' + key + r':\s*$$)([\s\S]*?)(\s*$$)'
    def rep(m):
        return m.group(1) + m.group(2).rstrip() + ', ' + v + '\n  ' + m.group(3)
    return re.sub(pattern, rep, html)

def main():
    today = datetime.today().strftime("%m/%d")
    path = os.path.expanduser("~/Desktop/dashboard.html")
    y2, y5, y10 = get_rates()
    fx = get_fx()
    tga = get_tga()
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    if '"' + today + '"' in html:
        print("오늘(" + today + ") 데이터가 이미 있습니다.")
        return
    html = add_value(html, "dates", today, is_str=True)
    html = add_value(html, "tga", tga)
    html = add_value(html, "y2", y2)
    html = add_value(html, "y5", y5)
    html = add_value(html, "y10", y10)
    html = add_value(html, "fx", fx)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("완료! " + today + " 데이터 추가됨. 브라우저 새로고침(CMD+R) 하세요.")

main()
