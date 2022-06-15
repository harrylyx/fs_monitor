from datetime import date
import yaml
from config.read import (
    get_fund_code,
    get_stock_code,
    get_coin_code,
    get_remind_fs_conf,
    get_stock_min_code,
)
from core import FundData, StockData, DigitalCoinData, StockMinData


def get_data(fund_code_set, stock_code_set, remind_fs_conf) -> list:
    data_dict = {}
    for fund_code in fund_code_set:
        fund_data = FundData(fund_code, remind_fs_conf[fund_code])
        fund_data.load()
        fund_data.transform()
        data_dict[fund_code] = fund_data
    for stock_code in stock_code_set:
        stock_data = StockData(stock_code, remind_fs_conf[stock_code])
        stock_data.load()
        stock_data.transform()
        data_dict[stock_code] = stock_data
    return data_dict


def get_coin_data(coin_set, remind_fs_conf) -> list:
    data_dict = {}
    for coin_code in coin_set:
        coin_data = DigitalCoinData(coin_code, remind_fs_conf[coin_code])
        coin_data.load()
        coin_data.transform(15)
        data_dict[coin_code + "_15"] = coin_data
    return data_dict


def get_stock_min_data(stock_code_set, remind_fs_conf) -> list:
    data_dict = {}
    for stock_code in stock_code_set:
        stock_data = StockMinData(stock_code, remind_fs_conf[stock_code])
        stock_data.load()
        stock_data.transform()
        data_dict[stock_code] = stock_data
    return data_dict


if __name__ == "__main__":
    remind_fs_conf = get_remind_fs_conf()
    coin_set = get_stock_min_code()
    data_dict = get_stock_min_data(coin_set, remind_fs_conf)
    for k, v in data_dict.items():
        print(k, v.is_remind, v.remind_message)
    # fund_code_set = get_fund_code()
    # stock_code_set = get_stock_code()
    # data_dict = get_data(fund_code_set, stock_code_set)
    # print(data_dict)
