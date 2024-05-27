import requests


def fetch_token_ids(page):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 250,
        'page': page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [coin['id'] for coin in response.json()]
    else:
        print(f"Failed to retrieve data for page {page}")
        return []
    

def refresh_token_id_list():
    # Collect token IDs from the first 10 pages (1000 tokens)
    token_ids = []
    for page in range(1, 5):
        token_ids.extend(fetch_token_ids(page))

    # Print the list of first 1000 token IDs by market cap
    print(token_ids)

    # Write the token IDs to a text file
    with open('token_ids.txt', 'w') as file:
        for token_id in token_ids:
            file.write(f"{token_id}\n")

    print("Token IDs have been written to token_ids.txt")