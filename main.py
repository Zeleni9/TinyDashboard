

from pycoingecko import CoinGeckoAPI
coin_manager = CoinGeckoAPI()


search_trending = coin_manager.get_search_trending()
#print(search_trending)

trending_coins = search_trending['coins']
trending_exchanges = search_trending['exchanges']

# print(trending_coins)
# print(trending_exchanges)

print("--------------------- Search Trending -----------------------------------")
# Write out trending coins from searches -- popular at the moment
for coin in trending_coins:
    print(f"Trending coin: {coin['item']['name']} with MarketCap rank:{coin['item']['market_cap_rank']}")
print("----------------------------------------------------------------------------------")


# nfts = coin_manager.get_nfts_list()
# for nft in nfts:
#     print(nft)


#Gather first 400 tokens name-ids to request their market cap & 24h volume
#coin_list = []
# for i in range(20):
#     coin_list_page = coin_manager.get_coins(page=i)
#     for coin in coin_list_page:
#         coin_list.append(coin['id'])

# with open('coingecko_coin_names.txt', 'w') as f:
#     for line in coin_list:
#         f.write(f"{line}\n")


with open('coingecko_coin_names.txt') as f:
    coin_list = f.read().splitlines()


first_coins_list = coin_list[0:400]
second_coins_list = coin_list[400:800]
third_coins_list = coin_list[800:]

first_coins = coin_manager.get_price(ids=first_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD")
second_coins = coin_manager.get_price(ids=second_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD")
third_coins = coin_manager.get_price(ids=third_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD")


print("--------------------- 24h Volume > Market Cap -----------------------------------")
for coin_name, coin_data in first_coins.items():
    if  int(coin_data['usd_24h_vol']) > int(coin_data['usd_market_cap']):
        print(f"Market Cap:{int(coin_data['usd_market_cap']):,} $ and 24h volume: {int(coin_data['usd_24h_vol']):,} $ Token - {coin_name}")
for coin_name, coin_data in second_coins.items():
    if  int(coin_data['usd_24h_vol']) > int(coin_data['usd_market_cap']):
        print(f"Market Cap:{int(coin_data['usd_market_cap']):,} $ and 24h volume: {int(coin_data['usd_24h_vol']):,} $ Token - {coin_name}")
for coin_name, coin_data in third_coins.items():
    if  int(coin_data['usd_24h_vol']) > int(coin_data['usd_market_cap']):
        print(f"Market Cap:{int(coin_data['usd_market_cap']):,} $ and 24h volume: {int(coin_data['usd_24h_vol']):,} $ Token - {coin_name}")
print("----------------------------------------------------------------------------------")
