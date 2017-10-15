import fut

fut = fut.Core('maillogin', 'passwort', 'sicherheitsabfrge', debug=True)

items = fut.searchAuctions(ctype='player', level='gold')

#nations = fut.nations()
leagues = fut.leagues()
teams = fut.teams()
stadiums = fut.stadiums()
players = fut.players()
playestyles = fut.playstyles()