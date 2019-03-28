import requests
from bs4 import BeautifulSoup
import unidecode
import csv

csv_file = open('performance_data.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['player id', 'player name', 'player age', 'team', 'player position', 'squads', 'appearances', 'starts', 'goals', 'assists', 'yellows', 'double yellows', 'reds', 'subbed on', 'subbed off', 'ppg', 'minutes'])

# league_info = [{'name': 'premier-league', 'abb':'GB1', 'id':'189'}, {'name': 'championship', 'abb':'GB2', 'id':'189'}, {'name': 'league-one', 'abb':'GB3', 'id':'189'}, {'name': 'league-two', 'abb':'GB4', 'id':'189'}, {'name': 'scottish-premiership', 'abb':'SC1', 'id':'190'}, {'name': 'scottish-championship', 'abb':'SC2', 'id':'190'}, {'name': 'laliga', 'abb':'ES1', 'id':'147'}, {'name': 'laliga2', 'abb':'ES2', 'id':'147'}]

league_info = [{'name': 'league-one', 'abb':'GB3', 'id':'189'}, {'name': 'league-two', 'abb':'GB4', 'id':'189'}, {'name': 'scottish-premiership', 'abb':'SC1', 'id':'190'}, {'name': 'scottish-championship', 'abb':'SC2', 'id':'190'}]

data_type = input('What data would you like (all/league)?: ').lower()

season = (input('Which season data would you like?: '))

performance_urls = []

headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def league_performance_data():

    for item in league_info:

        page = 'https://www.transfermarkt.co.uk/' + item['name'] + '/startseite/wettbewerb/' + item['abb'] + '/plus/?saison_id=' + season
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        teams_html = pageSoup.find('div', {'class': 'responsive-table'}).find_all('tr', {'class': ['odd', 'even']})

        for team_html in teams_html:

            team_name = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1].text.lower().replace(' ', '-')
            team_id = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1]['id']
            url_accents = 'https://www.transfermarkt.com/' + team_name + '/leistungsdaten/verein/' + team_id + '/reldata/' + item['abb'] + '%26' + season + '/plus/1'
            url = unidecode.unidecode(url_accents)
            performance_urls.append(url)

def all_performance_data():

    for item in league_info:

        page = 'https://www.transfermarkt.co.uk/' + item['name'] + '/startseite/wettbewerb/' + item['abb'] + '/plus/?saison_id=' + season
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
        teams_html = pageSoup.find('div', {'class': 'responsive-table'}).find_all('tr', {'class': ['odd', 'even']})

        for team_html in teams_html:
            team_name = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1].text.lower().replace(' ', '-')
            team_id = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})[1]['id']
            url_accents = 'https://www.transfermarkt.co.uk/' + team_name + '/leistungsdaten/verein/' + team_id + '/reldata/%26' + season + '/plus/1'
            url = unidecode.unidecode(url_accents)
            performance_urls.append(url)

if data_type == 'all':
    all_performance_data()
else:
    league_performance_data()

for url in performance_urls:

    pageTree = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    players = pageSoup.find_all('tr', {'class': ['odd', 'even']})

    # loop through the rows, pull the performance data from the rows and add it to the csv

    for player in players:

        player_id = player.find('a', {'class': 'spielprofil_tooltip'})['id']
        player_name = player.find('a', {'class': 'spielprofil_tooltip'}).text
        player_name = unidecode.unidecode(player_name)
        player_age = player.find_all('td', {'class': 'zentriert'})[1].text

        team = pageSoup.find('h1', {'itemprop': 'name'}).text
        team = team.lstrip()
        team = team.rstrip()
        team = unidecode.unidecode(team)

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
        minutes = player.find('td', {'class': 'rechts'}).text.strip("'").replace('.', '').replace('-', '0')
        starts = int(appearances) - int(subbed_on)

        csv_writer.writerow([player_id, player_name, player_age, team, player_position, squads, appearances, starts, goals, assists, yellows, double_yellows, reds, subbed_on, subbed_off, ppg, minutes])

csv_file.close()