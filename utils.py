import requests

code = "601618"
code_name = "ZGZY"
st_dt = "2022-02-10"


url = f"https://api.doctorxiong.club/v1/stock/kline/day?code={code}&startDate={st_dt}&type=1"

fstr = "{0} price {1} {2} CNY"

r = requests.get(url).json()
for line in r["data"]:
    print(fstr.format(line[0], code_name, line[2]))
