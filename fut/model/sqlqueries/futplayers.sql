CREATE TABLE IF NOT EXISTS fut_players (
  ressourceId VARCHAR(15) NOT NULL,
  firstname VARCHAR(45) DEFAULT NULL,
  lastname VARCHAR(45) DEFAULT NULL,
  surname VARCHAR(45) DEFAULT NULL,
  rating INT(3) DEFAULT NULL,
  nationality INT(3) DEFAULT NULL,
  PRIMARY KEY (ressourceId)
)