import urllib2
from BeautifulSoup import BeautifulSoup as soup

teams = {'csk':"Chennai Super Kings","mi":"Mumbai Indians","kxip":"Kings XI Punjab","kkr":"Kolkata Knight Riders",\
         "rcb":"Royal Challengers Bangalore","srh":"Sunrisers Hyderabad","rr":"Rajasthan Royals","dd":"Delhi Daredevils"}
teamsAbbr = {"Chennai Super Kings":"csk","Mumbai Indians":"mi","Kings XI Punjab":"kxip","Kolkata Knight Riders":"kkr",\
         "Royal Challengers Bangalore":"rcb","Sunrisers Hyderabad":"srh","Rajasthan Royals":"rr","Delhi Daredevils":"dd"}

page = urllib2.urlopen("http://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches").read()
soupedPage = soup(page)
teamsPage = soupedPage.findAll( "div", {"class": "cb-col-75 cb-col"} )

MatchesDataInOrder = []
for totalScenarios in range( len( teamsPage ) ):
    AvsB = teamsPage[totalScenarios].find( "span" )
    WinningTeam = teamsPage[totalScenarios].find( "a", {"class": "cb-text-link"} )
    team1,team2 = map(teamsAbbr.get,map(str.strip,map(str,AvsB.contents[0].split(",")[0].split(" vs "))))
    if WinningTeam!=None:
        winner = teamsAbbr[str(WinningTeam.contents[0].split("won")[0]).strip()]
    else:
        winner = "NP"
    MatchesDataInOrder.append([team1,team2,winner])

pointsPerTeam = {}
totalScenarios = 0
positions = {}

for team in teams.keys():
    pointsPerTeam[team] = 0
    positions[team] = {"Qualifier":0,"Eliminator":0,"Out of tournament":0}

def updatePossibilities(pointsTable, index):

    if index == 0:
        pointsTable.sort(key=lambda x: x[1])
        pointsTable.reverse()

    if index == 7:
        allPoints = []
        for team in pointsTable:
            allPoints.append(team[0])
        for team,points in pointsTable:
            stat = allPoints.index(team)
            if stat<2:
                positions[team]['Qualifier'] += 1
            elif stat<4:
                positions[team]['Eliminator'] += 1
            else:
                positions[team]['Out of tournament'] += 1
    else:
        for i in range(index+1, 8):
            if pointsTable[index][1] == pointsTable[i][1]:
                pointsTable[index], pointsTable[i] = pointsTable[i], pointsTable[index]
                updatePossibilities(pointsTable, index+1)
                pointsTable[index], pointsTable[i] = pointsTable[i], pointsTable[index]

        updatePossibilities(pointsTable, index+1)

def findAllPossiblities(matchdata, index, totalMatches, pointsPerTeam):
    if index==totalMatches-1:
        updatePossibilities(zip(pointsPerTeam.keys(),pointsPerTeam.values()), 0)
        return
    team1,team2,winner = matchdata[index]
    if winner=='NP':
        pointsPerTeam[team1] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team1] -= 2

        pointsPerTeam[team2] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team2] -= 2

        pointsPerTeam[team2] += 1
        pointsPerTeam[team1] += 1
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team2] -= 1
        pointsPerTeam[team1] -= 1
    else:
        pointsPerTeam[winner] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[winner] -= 2
findAllPossiblities( MatchesDataInOrder[:len( MatchesDataInOrder ) - 4], 0, len( MatchesDataInOrder ) - 3, pointsPerTeam )

totalScenarios = 0
for stat in positions['csk']:
    totalScenarios += positions['csk'][stat]

print totalScenarios, "Scenarios Ran"
for key in positions:
    print teams[key].upper()
    for stat in positions[key]:
        print stat.upper(),"-->", positions[key][stat]*100 / float( totalScenarios ), "%"
    print