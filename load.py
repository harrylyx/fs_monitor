import yaml
from config.read import get_fund_code, get_stock_code
from core import FundData, StockData


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


if __name__ == "__main__":
    fund_code_set = get_fund_code()
    stock_code_set = get_stock_code()
    data_dict = get_data(fund_code_set, stock_code_set)
    print(data_dict)
