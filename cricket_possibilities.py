import urllib2
from BeautifulSoup import BeautifulSoup as soup

teams = {'csk':"Chennai Super Kings","mi":"Mumbai Indians","kxip":"Kings XI Punjab","kkr":"Kolkata Knight Riders",\
         "rcb":"Royal Challengers Bangalore","srh":"Sunrisers Hyderabad","rr":"Rajasthan Royals","dd":"Delhi Daredevils"}
teamsAbbr = {"Chennai Super Kings":"csk","Mumbai Indians":"mi","Kings XI Punjab":"kxip","Kolkata Knight Riders":"kkr",\
         "Royal Challengers Bangalore":"rcb","Sunrisers Hyderabad":"srh","Rajasthan Royals":"rr","Delhi Daredevils":"dd"}

page = urllib2.urlopen("http://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches").read()
soupedPage = soup(page)
teamsPage = soupedPage.findAll( "div", {"class": "cb-col-75 cb-col"} )
#datePage = soupedPage.findAll("div", {"class": '"cb-col-25 cb-col pad10"'})
MatchesDataInOrder = []
for i in range(len(teamsPage)):
    AvsB = teamsPage[i].find("span")
    WinningTeam = teamsPage[i].find( "a", {"class": "cb-text-link"} )
    team1,team2 = map(teamsAbbr.get,map(str.strip,map(str,AvsB.contents[0].split(",")[0].split(" vs "))))
    if WinningTeam!=None:
        winner = teamsAbbr[str(WinningTeam.contents[0].split("won")[0]).strip()]
    else:
        winner = "NP"
    MatchesDataInOrder.append([team1,team2,winner])
#for i in MatchesDataInOrder:
#    print i
pointsPerTeam = {}
for key in teams.keys():
    pointsPerTeam[key] = 0

i = 0
positions = {}
for team in teams.keys():
    positions[team] = {"Qualifier":0,"Eliminator":0,"OUT of tour":0}
def updatePossibilities(pointsTable):
    pointsTable.sort(key=lambda x:x[1])
    pointsTable.reverse()
    allPoints = []
    for team in pointsTable:
        allPoints.append(team[1])
    for team,points in pointsTable:
        stat = allPoints.index(points)
        if stat<2:
            positions[team]['Qualifier'] += 1
        elif stat<4:
            positions[team]['Eliminator'] += 1
        else:
            positions[team]['OUT of tour'] += 1
def findAllPossiblities(matchdata, index, totalMatches, pointsPerTeam):
    global i
    if index==totalMatches-1:
        i += 1
        if i%10**5==0:
            print i,"cases ran"
        updatePossibilities(zip(pointsPerTeam.keys(),pointsPerTeam.values()))
        return
    team1,team2,winner = matchdata[index]
    if winner=='NP':
        pointsPerTeam[team1] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team1] -= 2

        pointsPerTeam[team2] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team2] -= 2

        pointsPerTeam[team1] += 1
        pointsPerTeam[team2] += 1
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[team1] -= 1
        pointsPerTeam[team2] -= 1
    else:
        pointsPerTeam[winner] += 2
        findAllPossiblities( matchdata, index + 1, totalMatches, pointsPerTeam )
        pointsPerTeam[winner] -= 2
findAllPossiblities( MatchesDataInOrder[:len( MatchesDataInOrder ) - 4], 0, len( MatchesDataInOrder ) - 3, pointsPerTeam )
print "Total Possibilities --> ", i
for key in positions:
    print teams[key],
    for stat in positions[key]:
        print stat,"->",positions[key][stat],"\t",
    print "possibility for playoff%:",(positions[key]['Eliminator']+positions[key]['Qualifier'])*100/float(i)