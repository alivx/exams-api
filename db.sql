-- Database export via SQLPro (https://www.sqlprostudio.com/allapps.html)
-- Exported by alib at 16-04-2021 14:00.
-- WARNING: This file may contain descructive statements such as DROPs.
-- Please ensure that you are running the script at the proper location.


-- BEGIN TABLE exams
DROP TABLE IF EXISTS exams;
CREATE TABLE `exams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numb` int(11) DEFAULT NULL,
  `question` text NOT NULL,
  `answer` text NOT NULL,
  `options` text NOT NULL,
  `material` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table exams contains no data. No inserts have been genrated.
-- Inserting 0 rows into exams


-- END TABLE exams

