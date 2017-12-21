CREATE TABLE IF NOT EXISTS fut_packs (
  id INT(5) NOT NULL,
  coins INT(10) DEFAULT NULL,
  points INT(10) DEFAULT NULL,
  quantity INT(3) DEFAULT NULL,
  saleType VARCHAR(15) DEFAULT NULL,
  isPremium VARCHAR(5) NOT NULL,
  InfoItemQuantity INT(3) DEFAULT NULL,
  GoldQuantity INT(3) DEFAULT NULL,
  SilverQuantity INT(3) DEFAULT NULL,
  BronzeQuantity INT(3) DEFAULT NULL,
  RareQuantity INT(3) DEFAULT NULL,
  start INT(12) DEFAULT NULL,
  ends INT(12) DEFAULT NULL,
  creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (id) references fut_desc(id)
)