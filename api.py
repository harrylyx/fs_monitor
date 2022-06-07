import time
import json
import requests


def fund_xiaoxiong(fund_code, st_dt):
    url = f"https://api.doctorxiong.club/v1/fund/detail?code={fund_code}&startDate={st_dt}"
    r = requests.get(url).json()
    if r["code"] == 200:
        return r["data"]
    else:
        raise Exception(
            f"fund_xiaoxiong error, fund_code:{fund_code}, code: {r['code']}"
        )


def fund_dongfang(fund_code):
    url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
    r = requests.get(url).text
    if len(r) > 10:
        r = json.loads(r[8:-2])
        return r
    else:
        raise Exception(f"fund_dongfang error, fund_code:{fund_code}, resp: {r}")


def stock_kline_xiaoxiong(stock_code, st_dt):
    url = f"https://api.doctorxiong.club/v1/stock/kline/day?code={stock_code}&startDate={st_dt}&type=1"
    r = requests.get(url).json()
    if r["code"] == 200:
        return r["data"]
    else:
        raise Exception(f"stock_kline_xiaoxiong error, code: {r['code']}")


def stock_info_xiaoxiong(stock_code):
    url = f"https://api.doctorxiong.club/v1/stock?code={stock_code}"
    r = requests.get(url).json()
    if r["code"] == 200:
        return r["data"]
    else:
        raise Exception(f"stock_info_xiaoxiong error, code: {r['code']}")


def digital_coin_coincap(coin_code):
    now = int(time.time())
    now -= now % 60
    now *= 1000
    url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=m1&baseId={coin_code}&quoteId=tether&start={now - 1500000}&end={now}"
    r = requests.get(url).json()
    if "data" in r:
        return r["data"]
    else:
        raise Exception(f"digital_coin_coincap error, {r}")


if __name__ == "__main__":
    data = digital_coin_coincap("binance-coin")
    print(len(data))
