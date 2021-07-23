DROP TABLE JournalEntries
DROP TABLE Moods


CREATE TABLE `JournalEntries` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `time` INTEGER,
  `concepts` TEXT NOT NULL,
  `entry` TEXT NOT NULL,
  `mood_id` INTEGER,
  FOREIGN KEY('mood_id') REFERENCES 'Moods'('id')
);

CREATE TABLE `Moods` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `mood` TEXT NOT NULL
);


INSERT INTO `JournalEntries` VALUES (null, 1626968542, "Love", "I love that lady", 1);
INSERT INTO `JournalEntries` VALUES (null, 1626967542, "Career", "I just got a rad job!",1);
INSERT INTO `JournalEntries` VALUES (null, 1626966542, "Friends", "Bill never paid me back for those tickets", 2);
INSERT INTO `JournalEntries` VALUES (null, 1626965542, "Love", "I hate that lady", 2);
INSERT INTO `JournalEntries` VALUES (null, 1626964542, "Career", "This job is only so-so", 3);


INSERT INTO `Moods` VALUES (null, 'Happy');
INSERT INTO `Moods` VALUES (null, 'Sad');
INSERT INTO `Moods` VALUES (null, 'Somewhere in the Middle');
INSERT INTO `Moods` VALUES (null, 'Anxious');

SELECT *
FROM JournalEntries j

SELECT *
FROM Moods m