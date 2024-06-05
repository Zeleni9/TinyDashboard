import streamlit as st
from pycoingecko import CoinGeckoAPI
import asyncio
import aiohttp


coin_manager = CoinGeckoAPI()


async def fetch_price(session, ids):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&include_market_cap=true&include_24hr_vol=true&vs_currencies=USD"
    async with session.get(url) as response:
        return await response.json()


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        search_trending = coin_manager.get_search_trending()
        
        with open("token_ids.txt") as f:
            coin_list = f.read().splitlines()
        
        tasks = []
        batch_size = 350
        for i in range(0, len(coin_list), batch_size):
            tasks.append(fetch_price(session, coin_list[i:i+batch_size]))
        
        results = await asyncio.gather(*tasks)
        
    return search_trending, results


def display_trending_coins(search_trending):
    trending_coins = search_trending["coins"]
    st.write("---")
    st.write("## Most Searched Tokens @ Coingecko")
    for coin in trending_coins:
        coin_id = coin["item"]["id"]
        coin_name = coin["item"]["name"]
        market_cap_rank = coin["item"]["market_cap_rank"]
        st.markdown(
            f"- [{coin_name}](https://www.coingecko.com/en/coins/{coin_id}) - MarketCap rank: **{market_cap_rank}**"
        )


def display_volume_data(coin_dict):
    for coin_name, coin_data in coin_dict.items():
        if coin_data:
            usd_market_cap = coin_data.get("usd_market_cap")
            usd_24h_vol = coin_data.get("usd_24h_vol")
            
            if usd_market_cap and usd_24h_vol:
                usd_market_cap = int(usd_market_cap)
                usd_24h_vol = int(usd_24h_vol)
                
                if usd_market_cap > 0 and usd_24h_vol > usd_market_cap:
                    st.write(
                        f"##### **{coin_name.capitalize()}** - [{coin_name}](https://www.coingecko.com/en/coins/{coin_name})"
                    )
                    st.markdown(f"- Market Cap: **{usd_market_cap:,} \$**")
                    st.markdown(f"- 24h Volume: **{usd_24h_vol:,} \$**")


def main():    
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
    search_trending, results = asyncio.run(fetch_data())
    
    display_trending_coins(search_trending)

    st.write("---")
    st.write("### 24h Volume Higher than MarketCap")
    for result in results:
        display_volume_data(result)

if __name__ == "__main__":
    main()
