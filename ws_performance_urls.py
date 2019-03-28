import requests
from bs4 import BeautifulSoup

league_url_end = ['GB1', 'GB2', 'GB3', 'GB4', 'SC1', 'SC2', 'ES1', 'ES2', 'IT1', 'IT2', 'FR1', 'FR2']

urls = []

# loop through each league and from the table collect the team names and their ids
# This will then make up the performance urls

for league_url in league_url_end:

    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = 'https://www.transfermarkt.co.uk/jumplist/startseite/wettbewerb/' + league_url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    # find the table html where the teams names are located

    teams_html = pageSoup.find('div', {'class': 'responsive-table'}).find_all('tr', {'class': ['odd', 'even']})

    for team_html in teams_html:

        teams_names_location = team_html.find_all('a', {'class': 'vereinprofil_tooltip'})
        teams_names = teams_names_location[1]
        teams_ids = teams_names['id']
        league = pageSoup.find('h1', {'class': 'spielername-profil'})
        teams_names_lower = teams_names.text.lower()
        teams_names_done = teams_names_lower.replace(' ', '-')
        url = 'https://www.transfermarkt.co.uk/' + teams_names_done + '/leistungsdaten/verein/' + teams_ids + '/reldata/%262018/plus/1'
        url_complete = url.replace('é', 'e').replace('á','a').replace('ñ', 'n').replace('ó', 'o').replace('í', 'i').replace('à', 'a').replace('î','i').replace('â', 'a')
        urls.append(url_complete)

for url in urls:
    print(url)