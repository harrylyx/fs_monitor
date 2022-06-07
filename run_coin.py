import time
import load
from datetime import datetime
from config.read import (
    get_remind_conf,
    get_coin_code,
    get_remind_fs_conf,
)
from remind import WeChat


def run():
    # load conf
    coin_code_set = get_coin_code()
    remind_conf = get_remind_conf()
    remind_fs_conf = get_remind_fs_conf()

    # load data
    data_dict = load.get_coin_data(coin_code_set, remind_fs_conf)
    print(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        [v.remind_message for k, v in data_dict.items()],
        file=open("/root/fs_monitor/run_coin.log", "a"),
    )

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
