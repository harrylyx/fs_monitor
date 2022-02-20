import requests

code = "000983"
code_name = "SXJM"
st_dt = "2022-02-10"


url_kline = f"https://api.doctorxiong.club/v1/stock/kline/day?code={code}&startDate={st_dt}&type=1"
url = f"https://api.doctorxiong.club/v1/stock?code={code}"

fstr = "{0} price {1} {2} CNY"

r_kline = requests.get(url_kline).json()
r = requests.get(url).json()
for line in r_kline["data"][:-1]:
    print(fstr.format(line[0], code_name, line[2]))
print(fstr.format(r_kline["data"][-1][0], code_name, r["data"][0]["price"]))
