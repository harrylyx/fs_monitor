from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from api import (
    fund_dongfang,
    fund_xiaoxiong,
    stock_info_xiaoxiong,
    stock_kline_xiaoxiong,
    digital_coin_coincap,
    stock_min_xiaoxiong,
)


class FinanceData(ABC):
    def __init__(self, code, user_list) -> None:
        self.code = code
        self.data_type = None
        self.source = None
        self.name = None
        self.raw_data = None
        self.yesterday_worth = None  # 昨日价格
        # self.yesterday_growth = None  # 昨日涨幅
        self.worth = None  # 当前价格
        self.growth = None  # 日涨幅
        self.is_remind = False  # 是否提醒
        self.remind_user = user_list  # 提醒用户
        self.remind_message = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.code}, {self.name},{self.data_type}, {self.source})"

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def transform(self):
        pass


class FundData(FinanceData):
    def __init__(self, code, user_list) -> None:
        super().__init__(code, user_list)
        self.data_type = "fund"

    def load(self):
        st_dt = datetime.strftime(datetime.now() - timedelta(days=7), "%Y-%m-%d")
        try:
            res = fund_dongfang(self.code)
            self.source = "dongfang"
        except:
            res = fund_xiaoxiong(self.code, st_dt)
            self.source = "xiaoxiong"
        self.raw_data = res
        self.name = self.raw_data["name"]

    def transform(self):
        if self.source == "dongfang":
            self.yesterday_worth = self.raw_data["dwjz"]
            self.worth = self.raw_data["gsz"]
            self.growth = self.raw_data["gszzl"]
        elif self.source == "xiaoxiong":
            self.yesterday_worth = self.raw_data["netWorth"]
            # self.yesterday_growth = self.raw_data["dayGrowth"]
            self.worth = self.raw_data.get("expectWorth")
            self.growth = self.raw_data.get("expectGrowth")
        else:
            raise Exception(f"source error, source is {self.source}")
        if self.growth and float(self.growth) < 0:
            self.is_remind = True
        self.remind_message = f"""基金名称：{self.name}
            基金代码：{self.code}
            当前基金单位净值估算： {self.worth}
            当前基金单位净值估算日涨幅： {self.growth}%
        """.replace(
            " ", ""
        )


class StockData(FinanceData):
    def __init__(self, code, user_list) -> None:
        super().__init__(code, user_list)
        self.data_type = "stock"

    def load(self):
        st_dt = datetime.strftime(datetime.now() - timedelta(days=7), "%Y-%m-%d")
        info = stock_info_xiaoxiong(self.code)[0]
        kline = stock_kline_xiaoxiong(self.code, st_dt)
        info["kline"] = kline
        self.source = "xiaoxiong"
        self.raw_data = info

    def transform(self):
        self.worth = self.raw_data["price"]
        self.growth = self.raw_data["changePercent"]
        self.yesterday_worth = self.raw_data["close"]
        # self.yesterday_growth = self.raw_data["changePercent"]
        self.name = self.raw_data["name"]
        if float(self.growth) < 0:
            self.is_remind = True
        self.remind_message = f"""股票名称：{self.name}
            股票代码：{self.code}
            收盘价： {self.worth}
            涨幅： {self.growth}%
        """.replace(
            " ", ""
        )


class StockMinData(FinanceData):
    def __init__(self, code, user_list) -> None:
        super().__init__(code, user_list)
        self.data_type = "stock"

    def load(self):
        min_info = stock_min_xiaoxiong(self.code)
        self.source = "xiaoxiong"
        self.raw_data = min_info

    def transform(self):
        buy = self.raw_data["buy"]
        self.name = self.raw_data["name"]
        if float(buy[1]) < 600000:
            self.is_remind = True
        self.remind_message = f"""股票名称：{self.name}
            股票代码：{self.code}
            买1： {buy[0]}： {buy[1]}
        """.replace(
            " ", ""
        )


class DigitalCoinData(FinanceData):
    def __init__(self, code, user_list) -> None:
        super().__init__(code, user_list)
        self.data_type = "digital_coin"

    def load(self):
        self.source = "coincap"
        self.raw_data = digital_coin_coincap(self.code)

    def transform(self, minute: int):
        assert len(self.raw_data) >= minute
        self.worth = float(self.raw_data[-1]["close"])
        self.yesterday_worth = float(self.raw_data[-minute]["close"])
        self.growth = ((self.worth - self.yesterday_worth) / self.yesterday_worth) * 100
        # self.yesterday_growth = self.raw_data["changePercent"]
        if self.growth >= 1 or self.growth <= -1:
            self.is_remind = True
        self.remind_message = f"""币名称：{self.code}
            {minute}分钟前收盘价： {self.yesterday_worth}
            当前价格： {self.worth}
            涨跌幅： {self.growth:0.4}%
        """.replace(
            " ", ""
        )
