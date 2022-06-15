import yaml
from pathlib import Path

root_path = Path(__file__).parent


def get_coin_code():
    with open(root_path / "coin.yaml", "r") as f:
        config = yaml.safe_load(f)
    coin_code_set = set()
    for name, coin_list in config.items():
        coin_code_set |= set(coin_list)
    return coin_code_set


def get_fund_code():
    with open(root_path / "fund.yaml", "r") as f:
        config = yaml.safe_load(f)
    fund_code_set = set()
    for name, fund_list in config.items():
        fund_code_set |= set(fund_list)
    return fund_code_set


def get_stock_code():
    with open(root_path / "stock.yaml", "r") as f:
        config = yaml.safe_load(f)
    stock_code_set = set()
    for name, stock_list in config.items():
        stock_code_set |= set(stock_list)
    return stock_code_set


def get_stock_min_code():
    with open(root_path / "stock_min.yaml", "r") as f:
        config = yaml.safe_load(f)
    stock_code_set = set()
    for name, stock_list in config.items():
        stock_code_set |= set(stock_list)
    return stock_code_set


def get_remind_fs_conf():
    with open(root_path / "fund.yaml", "r") as f:
        config_fund = yaml.safe_load(f)
    with open(root_path / "stock.yaml", "r") as f:
        config_stock = yaml.safe_load(f)
    with open(root_path / "coin.yaml", "r") as f:
        config_coin = yaml.safe_load(f)
    remind_dict = dict()
    for config_dict in [config_fund, config_stock, config_coin]:
        for k, v in config_dict.items():
            for i in v:
                remind_dict.setdefault(i, [])
                remind_dict[i].append(k)
    return remind_dict


def get_wechat_conf():
    with open(root_path / "wechat.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def get_remind_conf():
    with open(root_path / "remind.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


def get_code2name_conf():
    with open(root_path / "code2name.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config


if __name__ == "__main__":
    print(get_remind_fs_conf())
