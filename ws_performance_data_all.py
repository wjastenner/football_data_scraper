import requests
from bs4 import BeautifulSoup
import csv
import unidecode

csv_file = open('performance_data.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['player id', 'player name', 'player position', 'squads', 'appearances', 'starts', 'goals', 'assists', 'yellows', 'double yellows', 'reds', 'subbed on', 'subbed off', 'ppg', 'minutes'])

league_url_end = ['GB1', 'GB2', 'GB3', 'GB4', 'SC1', 'SC2', 'ES1', 'ES2', 'IT1', 'IT2', 'FR1', 'FR2', 'L1', 'L2']

performance_urls = []

headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# loop through the league_url_ends and create urls for the leagues interested in

for league_url in league_url_end:

    page = 'https://www.transfermarkt.co.uk/jumplist/startseite/wettbewerb/' + league_url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    # find the table and rows (odd, even) html where the team names and ids are located

    teams_html = pageSoup.find('div', {'class': 'responsive-table'}).find_all('tr', {'class': ['odd', 'even']})

    # for each row in the table locate the teams name and id and use these to create the new url list

    for team_html in teams_html:

        team_name = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1].text.lower().replace(' ', '-')
        team_id = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1]['id']
        url_accents = 'https://www.transfermarkt.co.uk/' + team_name + '/leistungsdaten/verein/' + team_id + '/reldata/%262018/plus/1'
        url = unidecode.unidecode(url_accents)
        performance_urls.append(url)

# loop through the performance urls created and find the html for the rows of data

for url in performance_urls:

    pageTree = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    players = pageSoup.find_all('tr', {'class': ['odd', 'even']})

    # loop through the rows, pull the performance data from the rows and add it to the csv

    for player in players:

        player_id = player.find('a', {'class': 'spielprofil_tooltip'})['id']
        player_name_accents = player.find('a', {'class': 'spielprofil_tooltip'}).text
        player_name = unidecode.unidecode(player_name_accents)

        team = pageSoup.find('h1', {'itemprop': 'name'}).text

        player_position = player.find('table', {'class': 'inline-table'}).find_all('tr', {'': ''})[1].text
        squads = player.find_all('td', {'class': 'zentriert'})[3].text.replace('-', '0')
        appearances = player.find_all('td', {'class': 'zentriert'})[4].text.replace('Was not used during this season', '0').replace('Not in squad during this season', '0')

        goals = player.find_all('td', {'class': 'zentriert'})[5].text.replace('-', '0')
        assists = player.find_all('td', {'class': 'zentriert'})[6].text.replace('-', '0')

        yellows = player.find_all('td', {'class': 'zentriert'})[7].text.replace('-', '0')
        double_yellows = player.find_all('td', {'class': 'zentriert'})[8].text.replace('-', '0')
        reds = player.find_all('td', {'class': 'zentriert'})[9].text.replace('-', '0')

        subbed_on = player.find_all('td', {'class': 'zentriert'})[10].text.replace('-', '0')
        subbed_off = player.find_all('td', {'class': 'zentriert'})[11].text.replace('-', '0')

        ppg = player.find_all('td', {'class': 'zentriert'})[12].text.replace(',', '.')
        minutes = player.find('td', {'class': 'rechts'}).text.strip("'").replace('-', '0')
        starts = int(appearances) - int(subbed_on)

        csv_writer.writerow([player_id, player_name, player_position, squads, appearances, starts, goals, assists, yellows, double_yellows, reds, subbed_on, subbed_off, ppg, minutes])