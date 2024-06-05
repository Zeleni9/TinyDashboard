import streamlit as st
from pycoingecko import CoinGeckoAPI
import asyncio
import aiohttp
import time

coin_manager = CoinGeckoAPI()


async def fetch_price(session, ids):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&include_market_cap=true&include_24hr_vol=true&vs_currencies=USD"
    async with session.get(url) as response:
        data = await response.json()
        if "error_code" in data and data["error_code"] == 429:
            st.error("Rate limit exceeded. Retrying in 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds before retrying
            async with session.get(url) as retry_response:
                data = await retry_response.json()
        return data

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        search_trending = coin_manager.get_search_trending()
        
        with open("token_ids.txt") as f:
            coin_list = f.read().splitlines()
        
        tasks = []
        
        # Define specific batch sizes
        batch_sizes = [400, 400, 200]
        start = 0
        for batch_size in batch_sizes:
            end = start + batch_size
            tasks.append(fetch_price(session, coin_list[start:end]))
            start = end
        
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
            if "error_code" in coin_data and coin_data["error_code"] == 429:
                st.warning(f"Rate limit exceeded for {coin_name}. Please try again later.")
                continue
            
            usd_market_cap = int(coin_data["usd_market_cap"])
            usd_24h_vol = int(coin_data["usd_24h_vol"])
            
            if usd_market_cap and usd_24h_vol:
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
