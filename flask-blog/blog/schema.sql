BEGIN TRANSACTION;
DROP TABLE IF EXISTS "post";
CREATE TABLE IF NOT EXISTS "post" (
	"id"	INTEGER,
	"author_id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"body"	TEXT NOT NULL,
	FOREIGN KEY("author_id") REFERENCES "user"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "user";
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"firstname"	TEXT,
	"lastname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "post" ("id","author_id","created","title","body") VALUES (1,1,'2020-12-30 14:09:01','Post 1','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pulvinar sapien sit amet nunc mollis, ut sagittis nunc venenatis. Maecenas finibus orci sit amet nisl tempus, at suscipit diam condimentum.');
INSERT INTO "post" ("id","author_id","created","title","body") VALUES (2,2,'2020-12-30 14:09:01','Post 2','Mauris pharetra, felis in ornare aliquam, lectus nisl tristique lorem, ut pellentesque diam tortor quis lorem. Nulla pulvinar interdum quam, sit amet porttitor neque condimentum id.');
INSERT INTO "post" ("id","author_id","created","title","body") VALUES (3,3,'2020-12-30 14:09:01','Post 3','Morbi sed iaculis dolor. Fusce at eros orci. Mauris eget pellentesque odio. Aenean interdum lectus libero, suscipit lacinia turpis lobortis et.');
INSERT INTO "post" ("id","author_id","created","title","body") VALUES (4,2,'2020-12-30 14:09:01','My Post','Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer pulvinar sapien sit amet nunc mollis, ut sagittis nunc venenatis. Maecenas finibus orci sit amet nisl tempus, at suscipit diam condimentum.');
INSERT INTO "user" ("id","username","password","firstname","lastname") VALUES (1,'bert','1234',NULL,NULL);
INSERT INTO "user" ("id","username","password","firstname","lastname") VALUES (2,'cookie','1234',NULL,NULL);
INSERT INTO "user" ("id","username","password","firstname","lastname") VALUES (3,'ernie','1234',NULL,NULL);
COMMIT;
