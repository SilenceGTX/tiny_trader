# -*- coding: UTF-8 -*-
"""
交易策略
"""

class Strategy:
    """
    交易策略类
    """
    def __init__(self, pos_lmt=0):
        """
        初始化
        
        参数：
            pos_lmt (int): 最高仓位限制（手），即持仓不能超过此数值。设置为0则代表无限制
        """
        self._position = 0 # 仓位
        self._pos_lmt = pos_lmt # 最高持仓限制
    
    def open_position(self, signal, price, lot):
        """
        开仓/加仓
        
        参数：
            signal (Signal): 信号类，用于发出买入/卖出信号
            price (float): 买入的价格
            lot (int): 买入多少手（1手即100股）
            
        返回：
            res (dict): 所执行交易的详细信息
        """
        res = {}
        s = signal.evaluate() # 评估看是否有买入信号
        
        if s is True:
            if (self._pos_lmt > 0 and self._position < self._pos_lmt) or self._pos_lmt == 0: # 尚未达到仓位限制
                self._position += lot
                res['operation'] = 'buy'
                res['price'] = price
                res['lot'] = lot
                res['position'] = self._position
        return res

    def take_profit(self, signal, price, lot=None):
        """
        止盈
        
        参数：
            signal (Signal): 信号类，用于发出买入/卖出信号
            price (float): 买入的价格
            lot (int): 买入多少手（1手即100股），默认None，将全部卖出
                
        返回：
            res (dict): 所执行交易的详细信息
        """
        res = {}
        s = signal.evaluate() # 评估看是否有买入信号
        sell_lot = lot if lot is not None else self._position
        
        if s is True:
            if self._position > 0: # 尚未达到仓位限制
                self._position -= sell_lot
                res['operation'] = 'sell_tp'
                res['price'] = price
                res['lot'] = -1 * sell_lot
                res['position'] = self._position
        return res
    
    def stop_loss(self, signal, price, lot=None):
        """
        止损
        
        参数：
            signal (Signal): 信号类，用于发出买入/卖出信号
            price (float): 买入的价格
            lot (int): 买入多少手（1手即100股），默认None，将全部卖出
                
        返回：
            res (dict): 所执行交易的详细信息
        """
        res = {}
        s = signal.evaluate() # 评估看是否有买入信号
        sell_lot = lot if lot is not None else self._position
        
        if s is True:
            if self._position > 0: # 尚未达到仓位限制
                self._position -= sell_lot
                res['operation'] = 'sell_sl'
                res['price'] = price
                res['lot'] = -1 * sell_lot
                res['position'] = self._position
        return res
