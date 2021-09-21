# -*- coding: UTF-8 -*-
"""
交易策略
"""


class Strategy:
    """
    交易策略类
    """
    def __init__(self, op_sig, tp_sig, ls_sig=None, cash_lmt=0):
        """
        初始化
        
        参数：
            op_sig (Signal): 开仓/加仓信号类（传入类，而非实例）
            tp_sig (Signal): 止盈信号类（传入类，而非实例）
            ls_sig (Signal): 止损信号类（传入类，而非实例），默认None，将使用止盈信号
            cash_lmt (float): 总资金限制，默认为0，即无限制
        """
        self._op_sig = op_sig # 开仓/加仓信号
        self._tp_sig = tp_sig # 止盈信号
        self._ls_sig = ls_sig # 止损信号
        self._cash_lmt = cash_lmt # 资金限制
        self._position = 0 # 仓位
        
    def buy(self, price, lot):
        """
        买入操作
        
        参数：
            price (float): 买入的价格
            lot (int): 买入多少手（1手即100股）
            
        返回：
            res (dict): 所执行交易的详细信息
        """
        res = {}
        self._position += lot
        res['operation'] = 'buy'
        res['price'] = price
        res['lot'] = lot
        res['position'] = self._position
        return res
    
    def sell(self, price, lot=None):
        """
        卖出操作
        
        参数：
            price (float): 卖出的价格
            lot (int): 卖出多少手（1手即100股），默认None，将全部卖出
            
        返回：
            res (dict): 所执行交易的详细信息
        """
        if lot is None:
            lot = self._position
            
        res = {}
        self._position -= lot
        res['operation'] = 'sell'
        res['price'] = price
        res['lot'] = -1 * lot
        res['position'] = self._position
        return res
    
    def open_setting(self, op_prc, op_lot):
        """
        开仓/加仓参数设置
        
        参数：
            op_prc (float): 买入的价格
            op_lot (int): 买入多少手（1手即100股）
        """
        self._op_prc = op_prc
        self._op_lot = op_lot
        
    def take_profit_setting(self, tp_prc, tp_lot=None):
        """
        止盈参数设置
        
        参数：
            tp_prc (float): 卖出的价格
            tp_lot (int): 卖出多少手（1手即100股），默认None，将全部卖出
        """
        self._tp_prc = tp_prc
        self._tp_lot = tp_lot
        
    def loss_stop_setting(self, ls_prc, ls_lot=None):
        """
        止损参数设置
        
        参数：
            tp_prc (float): 卖出的价格
            tp_lot (int): 卖出多少手（1手即100股），默认None，将全部卖出
        """
        self._ls_prc = ls_prc
        self._ls_lot = ls_lot
    
    def run(self, hist_kline):
        """
        根据历史行情判断是否应当开仓/止盈/止损
        """
        # 评估信号
        op = self._op_sig(hist_kline).evaluate()
        tp = self._tp_sig(hist_kline).evaluate()
        if self._ls_sig is not None:
            ls = self._ls_sig(hist_kline).evaluate()
        
        # 执行操作
        res = {}
        if op is True:
            if self._cash_lmt == 0:
                res = self.buy(self._op_prc, self._op_lot)
            else:
                if self._cash_lmt > self._op_prc * self._op_lot * 100:
                    res = self.buy(self._op_prc, self._op_lot)
                    
        if tp is True:
            if self._position > 0:
                if self._tp_lot is None:
                    res = self.sell(self._tp_prc, self._position)
                    res.update({'operation': 'take_profit'})
                elif self._position - self._tp_lot > 0:
                    res = self.sell(self._tp_prc, self._tp_lot)
                    res.update({'operation': 'take_profit'})
                
        if self._ls_sig is not None:
            if ls is True:
                if self._position > 0: 
                    if self._ls_lot is None:
                        res = self.sell(self._ls_prc, self._position)
                        res.update({'operation': 'loss_stop'})
                    elif self._position - self._ls_lot > 0:
                        res = self.sell(self._ls_prc, self._ls_lot)
                        res.update({'operation': 'loss_stop'})
        
        return res
