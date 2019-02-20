import rqams
from rqams import AMS_Client

client = AMS_Client('ou.yu@ricequant.com','demo')

portfolio = client.portfolios[0]
asset_unit = client.asset_units[0]

print(client.asset_units)
print(client.portfolios)
print(client.get_asset_trades(portfolio))
print(client.get_portfolio_trades(asset_unit))
print(client.get_asset_unit_positions(asset_unit))
print(client.get_portfolios_positions(portfolio))