databaseHost="db"
databaseUser="root"
databasePassword="root"
databaseName="exams"
appPort=8000
appHost="0.0.0.0"

createTable="""
CREATE TABLE IF NOT EXISTS `exams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numb` bigint(20) DEFAULT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `options` text NOT NULL,
  `material` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `question` (`question`(20),`answer`(20)),
  UNIQUE KEY `question_2` (`question`(1000),`answer`(500)),
  UNIQUE KEY `question_3` (`question`(1000),`answer`(1000))
) ENGINE=InnoDB AUTO_INCREMENT=754 DEFAULT CHARSET=latin1;
"""