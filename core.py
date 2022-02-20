from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from api import (
    fund_dongfang,
    fund_xiaoxiong,
    stock_info_xiaoxiong,
    stock_kline_xiaoxiong,
)


class FinanceData(ABC):
    def __init__(self, code, user_list) -> None:
        self.code = code
        self.data_type = None
        self.source = None
        self.name = None
        self.raw_data = None
        self.netWorth = None  # 当前价格
        self.dayGrowth = None  # 日涨幅
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
        self.expectWorth = None  # 当前估值
        self.expectGrowth = None  # 估值涨幅

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
            self.netWorth = self.raw_data["dwjz"]
            self.expectWorth = self.raw_data["gsz"]
            self.dayGrowth = self.expectGrowth = self.raw_data["gszzl"]
        elif self.source == "xiaoxiong":
            self.netWorth = self.raw_data["netWorth"]
            self.dayGrowth = self.raw_data["dayGrowth"]
            self.expectWorth = self.raw_data.get("expectWorth")
            self.expectGrowth = self.raw_data.get("expectGrowth")
        else:
            raise Exception(f"source error, source is {self.source}")
        if self.expectGrowth and float(self.expectGrowth) < 0:
            self.is_remind = True
        self.remind_message = f"""基金名称：{self.name}
            基金代码：{self.code}
            当前基金单位净值估算： {self.expectWorth}
            当前基金单位净值估算日涨幅： {self.expectGrowth}%
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
        self.netWorth = self.raw_data["price"]
        self.dayGrowth = self.raw_data["changePercent"]
        self.name = self.raw_data["name"]
        if float(self.dayGrowth) < 0:
            self.is_remind = True
        self.remind_message = f"""股票名称：{self.name}
            股票代码：{self.code}
            收盘价： {self.netWorth}
            涨幅： {self.dayGrowth}%
        """.replace(
            " ", ""
        )