import load


def is_fall(fund_data):
    if fund_data["source"] == "xiaoxiong":
        if "expectGrowth" not in fund_data:
            return False
        expectGrowth = fund_data["expectGrowth"]
    elif fund_data["source"] == "dongfang":
        expectGrowth = fund_data["gszzl"]
    else:
        raise Exception(f"api_type error, api_type: {fund_data['api_type']}")
    if float(expectGrowth) < 0:
        return True
    return False


def fall_rule(fund_data_dict):
    remind_fund_set = set()
    for code, fund_data in fund_data_dict.items():
        if is_fall(fund_data):
            remind_fund_set.add(code)
    return remind_fund_set


if __name__ == "__main__":
    conf_name = "config/fund.yaml"
    fund_code_set = load.get_fund_code(conf_name)
    fund_data_dict = load.get_fund_data(fund_code_set)
    remind_fund_set = fall_rule(fund_data_dict)
    print(remind_fund_set)
