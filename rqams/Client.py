import requests
import json
import logging
import functools


# def login(username,password):
#     login_url = 'http://rqams.com/api/user/login'
#     data = dict(username=username,password=password)
#     r = requests.post(login_url,data=data)
# #     print(r.text)
#     return r.cookies['sid']

class AMS_Client():
    def __init__(self,username,password,logger=None,logger_level=logging.DEBUG,
                 base_url='http://rqams.ricequant.com'):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.logger = logger if logger else logging.getLogger('AMS_Client')
        self.logger.setLevel(logger_level)
        self.sid = None
        self.portfolios = [x['id'] for x in self.get_portfolios()['portfolios']]
        self.asset_units = [x['id'] for x in self.get_asset_units()['asset_units']]
    
    def login(self):
        self.logger.info("Try login. Username {}".format(self.username))
        
        login_url = '{}/api/user/login'.format(self.base_url)
        data = dict(username=self.username,password=self.password)
        r = requests.post(login_url,data=data)
        return r
        
    def _do(self, func, *args, **kwargs):
        resp = func(*args, **kwargs)
        login_resp = self.login()
        if login_resp.json()["code"] == 0:
            self.sid = login_resp.cookies['sid']
            self.logger.info("login success")
        else:
            return login_resp
        resp = func(*args, **kwargs)
        return resp
    
    def get_portfolios(self):
        '''
        List
        login required
        get all your portfolio_ids
        '''
        return self._do(self._get_portfolios)
    
    def get_asset_units(self):
        '''
        List
        login required
        get all your asset_unit_ids
        '''
        return self._do(self._get_asset_units)
     
    def get_asset_unit_positions(self,asset_unit_id,date):
        return self._do(self._get_asset_unit_positions,asset_unit_id,date)

    def get_portfolios_positions(self, portfolio_id,date):
        return self._do(self._get_portfolio_positions,portfolio_id,date)
    

    def get_asset_trades(self,asset_unit_id,start_date,end_date):
        return self._do(self._get_asset_trades,portfolio_id,start_date,end_date)
    
    def get_portfolio_trades(self,portfolio_id,start_date,end_date):
        return self._do(self._get_portfolio_trades,portfolio_id,start_date,end_date)
    
    def apply_trades(self,portfolio_id,trades,asset_type):
        return self._do(self._apply_trades,portfolio_id,trades,asset_type)
    
    def portfolio_snapshot(self, portfolio_id):
        return self._do(self._portfolio_snapshot,portfolio_id)
    
    def asset_unit_snapshot(self, asset_unit_id):
        return self._do(self._asset_unit_snapshot,asset_unit_id)
    
    def _get_portfolios(self,limit=100,view='summary'):
        portfolio_url = '{}/api/rqams/v1/portfolios'.format(self.base_url)
        params = dict(limit = limit,view = view)
        cookies = dict(sid=self.sid)
        r = requests.get(portfolio_url,params=params,cookies=cookies)
        return r.json()          
    
    def _get_asset_units(self,limit=100,view='summary'):
        asset_units_url = '{}/api/rqams/v1/asset_units'.format(self.base_url)
        params = dict(limit = limit,view = view)
        cookies = dict(sid=self.sid)
        r = requests.get(asset_units_url,params=params,cookies=cookies)
        return r.json() 
    
    def _get_asset_unit_positions(self,asset_unit_id,date,view='detail'):
        holding_url = '{}/api/rqams/v1/asset_units/{}/holdings?'.format(self.base_url,asset_unit_id)
        params = dict(date = date,view = view)
        cookies = dict(sid=self.sid)
        r = requests.get(holding_url,params=params,cookies=cookies)
        return r.json()
    
    def _get_portfolios_positions(self,portfolio_id,date,view='detail'):
        holding_url = '{}/api/rqams/v1/portfolios/{}/holdings?'.format(self.base_url,portfolio_id)
        params = dict(date = date,view = view)
        cookies = dict(sid=self.sid)
        r = requests.get(holding_url,params=params,cookies=cookies)
        return r.json()
    
    def _get_asset_trades(self,asset_unit_id,start_date,end_date):
        trades_url = '{}/api/rqams/v1/asset_units/{}/trades?'.format(self.base_url,asset_unit_id)
        params = dict(start_date = start_date,end_date = end_date)
        cookies = dict(sid=self.sid)
        r = requests.get(trades_url,params=params,cookies=cookies)
        return r.json()
    
    def _get_portfolio_trades(self,portfolio_id,start_date,end_date):
        trades_url = '{}/api/rqams/v1/portfolios/{}/trades?'.format(self.base_url,portfolio_id)
        params = dict(start_date = date,end_date = end_date)
        cookies = dict(sid=self.sid)
        r = requests.get(trades_url,params=params,cookies=cookies)
        return r.json()
    
    def _apply_trades(self,portfolio_id,trades,asset_type):
        url = '{}/api/rqams/v1/portfolios/{}/trades'.format(self.base_url,portfolio_id)
        cookies = dict(sid=self.sid)
        for t in range(len(trades)):
            trade = trades.iloc[t]
            payload = dict(
                datetime = trade.datetime,
                order_book_id = trade.order_book_id,
                symbol = trade.symbol,
                asset_type = asset_type,
                side = trade.side,
                last_quantity = int(trade.last_quantity),
                #JSON无法识别int64
                last_price = trade.last_price,
                transaction_cost = trade.transaction_cost
            )
            r = requests.post(url,json=payload,cookies=cookies)
            print(r.json())
        return 

    def _portfolio_snapshot(self, portfolio_id):
        url = '{}/api/rqams/v1/portfolios/{}/current_snapshot'.format(self.base_url,portfolio_id)
        cookies = dict(sid=self.sid)
        params = dict(view='detail',aggregation_key='asset_type')
        r = requests.get(url,params=params,cookies=cookies)
        return r.json()

    def _asset_unit_snapshot(self,asset_unit_id):
        url = '{}/api/rqams/v1/asset_units/{}/current_snapshot'.format(self.base_url,asset_unit_id)
        cookies = dict(sid=self.sid)
        params = dict(view='detail',aggregation_key='asset_type')
        r = requests.get(url,params=params,cookies=cookies)
        return r.json()

            



# #获取资产单元交易流水
# def get_asset_positions(cookies,assetid,date,view='detail'):
#     holding_url = 'http://rqams.com/api/rqams/v1/asset_units/{}/holdings?'.format(assetid)
#     params = dict(date = date,view = view)
#     cookies = dict(sid=cookies)
#     r = requests.get(holding_url,params=params,cookies=cookies)
#     return r.json()

# #获取组合交易流水
# def get_asset_positions(cookies,assetid,date,view='detail'):
#     holding_url = 'http://rqams.com/api/rqams/v1/asset_units/{}/holdings?'.format(assetid)
#     params = dict(date = date,view = view)
#     cookies = dict(sid=cookies)
#     r = requests.get(holding_url,params=params,cookies=cookies)
#     return r.json()

# #获取资产单元indicators
# def get_indicators():
#     pass

# #获取组合的的indicators
# def get_pf_indicators():
#     pass

