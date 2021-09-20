# -*- coding: UTF-8 -*-
"""
用于数据源获取
"""
from datetime import datetime
import json
import requests
import tushare as ts


# 配置
tk = json.load(open('token.json', 'r'))
token = tk['token']

ts.set_token(token)
pro = ts.pro_api(token)


# 其他辅助类/函数
class Tick:
    """
    存放某一时刻股价数据的容器类
    """
    def __init__(self, data):
        """
        初始化

        参数：
            data (str): 从新浪API获取的实时股价数据
        """
        self._raw = data
        
    def parse(self):
        """
        清理数据

        返回：
            res (dict): 处理后装入字典中的股价数据
        """
        raw_sp = self._raw.split(',')
        dt = raw_sp[-3] + ' ' + raw_sp[-2]
        name = raw_sp[0].replace('"', '').split('=')[1]
        
        op = float(raw_sp[1])
        last_cls = float(raw_sp[2])
        curr = float(raw_sp[3])
        hi = float(raw_sp[4])
        lw = float(raw_sp[5])
        bid_prc = float(raw_sp[6])
        ask_prc = float(raw_sp[7])
        txns = round(float(raw_sp[8]))
        trnovr = round(float(raw_sp[9]))
        bid1_qty = round(float(raw_sp[10]))
        bid1_prc = float(raw_sp[11])
        bid2_qty = round(float(raw_sp[12]))
        bid2_prc = float(raw_sp[13])
        bid3_qty = round(float(raw_sp[14]))
        bid3_prc = float(raw_sp[15])
        bid4_qty = round(float(raw_sp[16]))
        bid4_prc = float(raw_sp[17])
        bid5_qty = round(float(raw_sp[18]))
        bid5_prc = float(raw_sp[19])
        ask1_qty = round(float(raw_sp[20]))
        ask1_prc = float(raw_sp[21])
        ask2_qty = round(float(raw_sp[22]))
        ask2_prc = float(raw_sp[23])
        ask3_qty = round(float(raw_sp[24]))
        ask3_prc = float(raw_sp[25])
        ask4_qty = round(float(raw_sp[26]))
        ask4_prc = float(raw_sp[27])
        ask5_qty = round(float(raw_sp[28]))
        ask5_prc = float(raw_sp[29])

        res = {
            'name': name,
            'timestamp': dt,
            'open': op,
            'last_close': last_cls,
            'current_price': curr,
            'high': hi,
            'low': lw,
            'bid_price': bid_prc,
            'ask_price': ask_prc,
            'transactions': txns,
            'turnover': trnovr,
            'bid_quantity_1': bid1_qty,
            'bid_quantity_2': bid2_qty,
            'bid_quantity_3': bid3_qty,
            'bid_quantity_4': bid4_qty,
            'bid_quantity_5': bid5_qty,
            'bid_price_1': bid1_prc,
            'bid_price_2': bid2_prc,
            'bid_price_3': bid3_prc,
            'bid_price_4': bid4_prc,
            'bid_price_5': bid5_prc,
            'ask_quantity_1': ask1_qty,
            'ask_quantity_2': ask2_qty,
            'ask_quantity_3': ask3_qty,
            'ask_quantity_4': ask4_qty,
            'ask_quantity_5': ask5_qty,
            'ask_price_1': ask1_prc,
            'ask_price_2': ask2_prc,
            'ask_price_3': ask3_prc,
            'ask_price_4': ask4_prc,
            'ask_price_5': ask5_prc
        }
        return res


# 日线查询函数 (tushare)
def get_ts_stock_data(stock_code, start_date, end_date=None, freq='daily'):
    """
    从Tushare拉取单支个股的数据，默认日线数据

    参数：
        stock_code (str): 股票代码，须为'SZ000345'或'SH600231'形式
        start_date (str): 获取历史数据的起始日期，须为'20210625'形式
        end_date (str): 获取历史数据的结束日期，须为'20210625'形式，默认为None，将采用今天 
        freq (str): 数据频次，默认为daily（日线）
    
    返回：
        kline (DataFrame): K线数据
    """
    ts_stock_cd = f'{stock_code[2:]}.{stock_code[:2]}'
    if end_date is None:
        end_date = datetime.now().strftime('%Y%m%d')
    
    kline = pro.query(freq, ts_code=ts_stock_cd, start_date=start_date, end_date=end_date)
    kline['ts_code'] = stock_code.upper()
    return kline

# 即时查询函数（新浪）
def get_sina_stock_data(stock_code):
    """
    从新浪API拉取单支个股的实时数据

    参数：
        stock_code (str): 股票代码，须为'SZ000345'或'SH600231'形式

    返回：
        res (dict): 处理后装入字典中的股价数据
    """
    resp = requests.get(f'http://hq.sinajs.cn/list={stock_code.lower()}').text
    res = Tick(resp).parse()
    res.update({'code': stock_code.upper()})
    return res
