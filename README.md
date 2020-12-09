Update config.py with database connection info

Create table for DB below

CREATE TABLE `stats` (
  `id` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `ip` int(10) unsigned DEFAULT NULL,
  `skew` float DEFAULT NULL,
  `offset` float DEFAULT NULL,
  `stddev` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8
