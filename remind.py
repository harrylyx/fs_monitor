import time
import json
import requests
import load
from config.read import (
    get_wechat_conf,
    get_remind_conf,
    get_fund_code,
    get_stock_code,
    get_remind_fs_conf,
)

root_path = "./"


class WeChat:
    def __init__(self):
        conf = get_wechat_conf()
        self.CORPID = conf["CORPID"]  # 企业ID，在管理后台获取
        self.CORPSECRET = conf["CORPSECRET"]  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = conf["AGENTID"]  # 应用ID，在后台应用中获取
        self.TOUSER = "@all"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {
            "corpid": self.CORPID,
            "corpsecret": self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open(root_path + "tmp/access_token.conf", "r") as f:
                t, access_token = f.read().split()
        except:
            with open(root_path + "tmp/access_token.conf", "w") as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write("\t".join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open(root_path + "tmp/access_token.conf", "w") as f:
                    access_token = self._get_access_token()
                    f.write("\t".join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


def run():
    # load conf
    fund_code_set = get_fund_code()
    stock_code_set = get_stock_code()
    remind_conf = get_remind_conf()
    remind_fs_conf = get_remind_fs_conf()

    # load data
    data_dict = load.get_data(fund_code_set, stock_code_set, remind_fs_conf)

    # remind
    wechat = WeChat()

    for _, data in data_dict.items():
        if data.is_remind:
            for user in data.remind_user:
                for remind_method in remind_conf[user]:
                    if remind_method == "wechat":
                        wechat.send_data(data.remind_message)
                        time.sleep(1)


if __name__ == "__main__":
    run()
