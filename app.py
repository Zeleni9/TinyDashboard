import streamlit as st
from pycoingecko import CoinGeckoAPI

coin_manager = CoinGeckoAPI()


def display_tredning_coins(search_trending):
    trending_coins = search_trending["coins"]
    trending_exchanges = search_trending["exchanges"]
    st.write("---")
    st.write("### Most Searched Tokens @ Coingecko")
    for coin in trending_coins:
        coin_name = coin["item"]["name"]
        market_cap_rank = coin["item"]["market_cap_rank"]
        st.write(
            f" **{coin_name}**                 - MarketCap rank: {market_cap_rank} Coingecko URL: [{coin_name}](https://www.coingecko.com/en/coins/{coin_name})"
        )


def display_volume_data(coin_dict):
    for coin_name, coin_data in coin_dict.items():
        if int(coin_data["usd_24h_vol"]) > int(coin_data["usd_market_cap"]):
            usd_market_cap = int(coin_data["usd_market_cap"])
            usd_volume = int(coin_data["usd_24h_vol"])
            st.write(
                f"**{coin_name}** - Market Cap: {usd_market_cap:,} \$ - 24h Volume: {usd_volume:,}  \$ - Coingecko URL: [{coin_name}](https://www.coingecko.com/en/coins/{coin_name})"
            )


def fetch_data():
    search_trending = coin_manager.get_search_trending()

    with open("coingecko_coin_names.txt") as f:
        coin_list = f.read().splitlines()

    first_coins_list = coin_list[0:400]
    second_coins_list = coin_list[400:800]
    third_coins_list = coin_list[800:]

    first_coins = coin_manager.get_price(
        ids=first_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )
    second_coins = coin_manager.get_price(
        ids=second_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )
    third_coins = coin_manager.get_price(
        ids=third_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )

    display_tredning_coins(search_trending)

    st.write("---")
    st.write("### 24h Volume Higher than MarketCap")
    display_volume_data(first_coins)
    display_volume_data(second_coins)
    display_volume_data(third_coins)


# creating a single-element container.
placeholder = st.empty()


with placeholder.container():
    st.write("""# Trending Crpyto Currenices""")
    st.sidebar.write("## Application Settings")
    st.sidebar.write(
        """
        - The data is fetched from Coingecko API, it is free
        - Showing the most searched tokens on Coingecko
        - Showing tokens that have 24h volume bigger than marketcap
        - Fetching the first 1000 token by marketcap
        - Suggest new ideas as well"""
    )
    fetch_data()
