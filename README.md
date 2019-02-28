## RQAMS ##
使用用户名和密码进行初始
```python
from rqams import AMS_Client

client = AMS_Client(yourusername,yourpassword,base_url='https://rqams.ricequant.com')
```
获取所有的组合id
```python
client.portfolios
```
```python
['5c75f5b2713b78005a96a81d',
 '5c75f59b713b7800121270a9',
 '5c75f57f713b78006e01c0cc',
 '5c75f54d713b7800121270a8']
```
获取所有的资产单元id
```python
client.asset_units
```
```python
['5c75f724713b78005a96a81e',
 '5c75f6fd713b78006e01c0ce',
 '5c75f6be713b78006e01c0cd',
 '5c75f65e713b78001956d28e']
```
获取所有组合的信息，信息包含组合总数，组合名称，开始日期，组合id
```python
client.get_portfolios()
```
同理，获取所有资产单元信息，信息包含资产单元总数，资产单元名称，资产单元基准，资产单元初始资金，资产单元的id
```python
client.get_asset_units()
```
获取组合的交易流水，需要组合id
```python
client.get_portfolio_trades('5c6d0fb4b2f6a4070a1ad929',start_date='20180101',end_date='20190201')
```
```python
{'total_size': 233,
 'trades': [{'asset_type': 'stock',
   'datetime': '2017-01-13T15:00:00',
   'trading_date': '2017-01-13',
   'order_book_id': '601398.XSHG',
   'symbol': '工商银行',
   'last_quantity': 21200,
   'side': 'buy',
   'last_price': 4.45,
   'transaction_cost': 75.472,
   'portfolio': '5c6d0fb4b2f6a4070a1ad929',
   'id': '5c6d0fbeb2f6a4071af85c2a'},
  {'asset_type': 'stock',
   'datetime': '2017-01-13T15:00:00',
   'trading_date': '2017-01-13',
   'order_book_id': '601939.XSHG',
   'symbol': '建设银行',
   'last_quantity': 17300,
   'side': 'buy',
   'last_price': 5.47,
   'transaction_cost': 75.705,
   'portfolio': '5c6d0fb4b2f6a4070a1ad929',
   'id': '5c6d0fbeb2f6a4071af85c2b'},
   ....
```
同理，获取资产单元的交易流水，需要资产单元id
```python
client.get_asset_trades(asset_id,start_date,end_date)
```
获取资产单元的持仓情况
```python
client.get_asset_unit_positions('5c75f6be713b78006e01c0cd',date='20190101')
```
同理，获取组合的持仓情况
```python
client.get_portfolio_positions(portfolio_id,date)
```
传入交易：
请将交易流水或者交易准备成如下的DataFrame，可以通过apply_trades上传交易，上传后即可在AMS中看到。
```python
datetime	order_book_id	symbol	side	last_quantity	last_price	transaction_cost
0	2017/1/13 15:00	601398.XSHG	工商银行	buy	21200	4.45	75.472
1	2017/1/13 15:00	601939.XSHG	建设银行	buy	17300	5.47	75.705
2	2017/1/13 15:00	601288.XSHG	农业银行	buy	30400	3.11	75.635
```
```python
client.apply_trades(data)
```
获取资产单元的实时情况
```
client.asset_unit_snapshot(asset_unit_id)
```
```python
{'unit_net_value': 1.0367979784171286,
 'total_equity': 10367979.784171287,
 'market_value': 1279233.9921712875,
 'exposure': 0.12338314877159424,
 'day_pnl': -3516.005126953125,
 'cash': 9088745.792,
 'static_unit_net_value': 1.0371495791999998,
 'aggregations': [{'key': 'stock',
   'positions': [{'order_book_id': '601398.XSHG',
     'portfolio': '5c75098b5cd90e0c0f2b1fbb',
     'asset_type': 'stock',
     'direction': 'long',
     'quantity': 21600,
     'last_price': 5.739999771118164,
     'cost_price': 4.357122421264648,
     'cost': 94113.84,
     'day_pnl': -1512.0047607421875,
     'floating_pnl': 29870.150390625,
     'price_change': -0.07000017166137695,
     'price_change_rate': -0.012048222124576569,
     'market_value': 123983.99505615234,
     'avg_price': 4.357122421264648,
     'weight': 0.011958356173247727,
     'symbol': '工商银行',
     'timestamp': '2019-02-28 14:52:40'},
```
获取组合的实时情况
```
client.portfolio(portfolio_id)
```

