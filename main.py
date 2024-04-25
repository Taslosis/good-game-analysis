import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def fetch_game_stats(url):
    """
    Fetches and parses game statistics from a given URL, preparing it for visualization.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the webpage, status code:", response.status_code)
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    games = soup.find_all('tr')[1:11]

    game_data = []
    for game in games:
        columns = game.find_all('td')
        if len(columns) >= 5:
            try:
                name = columns[1].text.strip()
                current_players = int(columns[2].text.strip().replace(',', ''))
                game_info = {
                    'Name': name,
                    'Current Players': current_players
                }
                game_data.append(game_info)
            except ValueError as e:
                print(f"Error converting data: {e}")
                continue

    return pd.DataFrame(game_data)

def plot_current_players(data):
    """
    Plots a bar graph of the current players for each game.
    """
    if data.empty:
        return
    data.plot(kind='bar', x='Name', y='Current Players', color='blue', figsize=(10, 6))
    plt.xlabel('Game')
    plt.ylabel('Current Players')
    plt.title('Current Players per Game')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    url = "https://steamcharts.com/top"
    data = fetch_game_stats(url)
    if not data.empty:
        print(data)
        plot_current_players(data)

if __name__ == "__main__":
    main()
