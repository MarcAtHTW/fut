import fut
import json
from fut.model import dbConnector as DB

db = DB.Database()


q = "CREATE TABLE Player (id INT(6) " \
    "UNSIGNED AUTO_INCREMENT PRIMARY KEY, " \
    "firstname VARCHAR(30) NOT NULL," \
    "lastname VARCHAR(30) NOT NULL," \
    "position VARCHAR(50)," \
    "reg_date TIMESTAMP" \
    ")"


q = "INSERT INTO Player (firstname, lastname, position)" \
    "VALUES ('Christian', 'Auner', 'Mittelfeld')"

q = "SELECT * FROM Player"

#q = "SHOW DATABASES"
#q = "SHOW TABLES"

#result = db.insert(q)
#result = db.query(q)
#print(result)
fut = fut.Core('ps3@marc-sahib.de', 'EATempPass2017', 'seifert', debug=True)

items = fut.searchAuctions(ctype='player', level='gold')

dump = json.dumps(items)
#parsed = json.loads(items)
#print(json.dumps(parsed, indent=4, sort_keys=True))
#print(items)

#players = fut.players
#nations = fut.nations()

#leagues = fut.leagues()
#teams = fut.teams()
#stadiums = fut.stadiums()
#players = fut.players()
#playestyles = fut.playstyles()
print('Done')