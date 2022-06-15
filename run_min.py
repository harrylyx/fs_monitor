import time
import load
from config.read import (
    get_remind_conf,
    get_stock_min_code,
    get_remind_fs_conf,
)
from remind import WeChat
from save import save_to_beancount


def run():
    # load conf
    stock_code_set = get_stock_min_code()
    remind_conf = get_remind_conf()
    remind_fs_conf = get_remind_fs_conf()

    # load data
    data_dict = load.get_stock_min_data(stock_code_set, remind_fs_conf)
    print(data_dict["002939"].remind_message)

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
