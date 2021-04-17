import ccxt
# from variable id
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': '98mlIyVASCNtJk9twyoYwJSmAnqmMf7XmWpPvsPUEllsHemUAtxRKs44ykuo8rdv',
    'secret': 'aNDNqfWkZIZqEMME2OUMnAxvZujhkbMZgkGlVA4EbwdIB9JZccGJzFBkHR3VXkat',
    'timeout': 30000,
    'enableRateLimit': True,
})

print(exchange.load_markets())

etheurId = exchange.market_id('ETH/USDT')   # get market id by symbol

symbols = exchange.symbols                 # get a list of symbols
symbols2 = list(exchange.markets.keys())   # same as previous line

#print(exchange.id, symbols)                # print all symbols
print(etheurId)
currencies = exchange.currencies  




