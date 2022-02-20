import imp
import time
import load
from config.read import (
    get_remind_conf,
    get_fund_code,
    get_stock_code,
    get_remind_fs_conf,
)
from remind import WeChat
from save import save_to_beancount


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

    # save
    file_name = "/root/HomeAccount/accounts/price.bean"

    save_to_beancount(file_name, data_dict)


if __name__ == "__main__":
    run()
