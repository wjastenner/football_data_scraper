import requests
from bs4 import BeautifulSoup
import csv

urls = ['GB1', 'GB2', 'GB3', 'GB4', 'ES1', 'ES2', 'IT1', 'IT2', 'FR1', 'FR2']

csv_file = open('team_ids.csv', 'w')

csv_writer = csv.writer(csv_file)

csv_writer.writerow(['team', 'team_id', 'league'])

for url in urls:

    headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = 'https://www.transfermarkt.co.uk/jumplist/startseite/wettbewerb/' + url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    table_html = pageSoup.find('div', {'class': 'responsive-table'})
    teams_details = table_html.find_all('tr', {'class': ['odd', 'even']})

    for team in teams_details:

        teams_names_location = team.find_all('a', {'class': 'vereinprofil_tooltip'})
        teams_names = teams_names_location[1]
        teams_ids = teams_names['id']
        league = pageSoup.find('h1', {'class': 'spielername-profil'})

        print('')
        print(teams_names.text)
        print(teams_ids)
        print(league.text)
        csv_writer.writerow([teams_names.text, teams_ids, league.text])

csv_file.close()

