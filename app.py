import streamlit as st
from pycoingecko import CoinGeckoAPI

coin_manager = CoinGeckoAPI()


def display_trending_coins(search_trending):
    trending_coins = search_trending["coins"]
    st.write("---")
    st.write("## Most Searched Tokens @ Coingecko")
    for coin in trending_coins:
        coin_id = coin["item"]["id"]
        coin_name = coin["item"]["name"]
        market_cap_rank = coin["item"]["market_cap_rank"]
        st.markdown(
            f"- [{ coin_name}](https://www.coingecko.com/en/coins/{coin_id})  -  MarketCap rank:   **{market_cap_rank}** "
        )


def display_volume_data(coin_dict):
    for coin_name, coin_data in coin_dict.items():
        if coin_data and int(coin_data["usd_market_cap"]) > 0:
            if int(coin_data["usd_24h_vol"]) > int(coin_data["usd_market_cap"]):
                usd_market_cap = int(coin_data["usd_market_cap"])
                usd_volume = int(coin_data["usd_24h_vol"])
                st.write(
                    f"##### **{coin_name.capitalize()}** - [{coin_name}](https://www.coingecko.com/en/coins/{coin_name})"
                )
                st.markdown(f"- Market Cap: **{usd_market_cap:,} \$** ")
                st.markdown(f"- 24h Volume: **{usd_volume:,}  \$** ")


def fetch_data():
    search_trending = coin_manager.get_search_trending()

    with open("token_ids.txt") as f:
        coin_list = f.read().splitlines()

    first_coins_list = coin_list[0:350]
    second_coins_list = coin_list[350:700]
    third_coins_list = coin_list[700:]

    first_coins = coin_manager.get_price(
        ids=first_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )
    second_coins = coin_manager.get_price(
        ids=second_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )
    third_coins = coin_manager.get_price(
        ids=third_coins_list, include_market_cap=True, include_24hr_vol=True, vs_currencies="USD"
    )

    display_trending_coins(search_trending)

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
