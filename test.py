import rqams
from rqams import AMS_Client

client = AMS_Client('ou.yu@ricequant.com','demo')

portfolio = client.portfolios[0]
asset_unit = client.asset_units[0]
start_date = '20180101'
end_date = '20190203'




print(client.asset_units)
print(client.portfolios)
print(client.get_asset_trades(asset_unit,start_date=start_date,end_date=end_date))
print(client.get_portfolio_trades(portfolio,start_date=start_date,end_date=end_date))
# print(client.get_asset_unit_positions(asset_unit,date=end_date)
# )
# print(client.get_portfolios_positions(portfolio,date=end_date))