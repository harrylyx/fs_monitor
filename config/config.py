import yaml


def get_fund_code():
    with open("fund.yaml", "r") as f:
        config = yaml.safe_load(f)
    fund_code_set = set()
    for name, fund_list in config.items():
        fund_code_set |= set(fund_list)
    return fund_code_set


def get_stock_code():
    with open("stock.yaml", "r") as f:
        config = yaml.safe_load(f)
    stock_code_set = set()
    for name, stock_list in config.items():
        stock_code_set |= set(stock_list)
    return stock_code_set


def get_remind_conf():
    with open("remind.yaml", "r") as f:
        config = yaml.safe_load(f)
    remind_dict = dict()
    for k, v in config.items():
        for i in v:
            remind_dict.setdefault(i, [])
            remind_dict[i].append(k)
    return remind_dict
