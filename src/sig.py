# -*- coding: UTF-8 -*-
"""
交易信号
"""
from abc import ABC, abstractmethod


class Signal(ABC):
    """
    发出交易信号的基类（抽象类），所有策略由此派生
    """
    def __init__(self, kline):
        """
        初始化
        
        参数：
            kline (DataFrame): 历史K线数据（到昨天为止），可包含其他指标的计算结果
        """
        self._kline = kline
    
    @abstractmethod
    def evaluate(self):
        """
        评估条件，看是否发出买入/卖出信号
        
        返回：
            True/False: 是否发出信号
        """
        return False
