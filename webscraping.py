import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = input("Please enter URL: ")
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')


# collect all classes within the website named odd or even. These are then placed into a list called 'players'
players = pageSoup.find_all('tr', {'class':['odd', 'even']})

# loop through the html of the individual items (named in the for loop as 'player') within the 'players' list
# print the following information for each 'player': name, transfer fee, season, nationality and team

for player in players:
    print('')

    # within the player html find the tag 'a' and class="spielprofil_tooltip" and print the associated text
    player_name = player.find('a', {'class':'spielprofil_tooltip'}).text
    print(player_name)

    # within the player html find the tag 'td' and class="rechts hauptlink" and print the associated text
    transfer_fee = player.find('td', {'class': 'rechts hauptlink'}).text
    print(transfer_fee)

    # within the player html find all the 'td' tags where class="zentriert". Because there are more than 1 this creates
    # a list. The print statement prints the text associated to the second match within that list
    season = player.find_all('td', {'class': 'zentriert'})
    print(season[1].text)

    # within the player html the nationality is found within the third match where the tag equals 'td'
    # and where class="zentriert". This does not contain any text therefore we locate the 'img' tag and collect the
    # 'title' attribute
    nationality = season[2].find('img')
    nationality_title = nationality['title']
    print(nationality_title)

    # within the player html the team is found within the first 'a' tag where class="vereinprofil_tooltip".
    # This does not contain any text but it can be found by locating the 'img' tag and extracted from the 'alt' attribute
    team = player.find('a', {'class': 'vereinprofil_tooltip'})
    team_img = team.find('img')
    team_name = team_img['alt']
    print(team_name)

    # within the player html the league is found in the third 'td' in the second table where the class="inline-table"
    # This does not contain any text but it can be found by locating the 'a' tag and extracted from the 'title' attribute
    leagues = player.find_all('table', {'class':'inline-table'})
    league = leagues[1].find_all('td')
    try:
        league_name_location = league[2].find('a')
        league_name = league_name_location['title']
        print(league_name)
    except Exception:
        print("Unknown")