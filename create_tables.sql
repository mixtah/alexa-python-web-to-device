CREATE TABLE IF NOT EXISTS alexa_response (
	id			SERIAL		PRIMARY KEY,
	name	TEXT,
	link	TEXT,
	settings	TEXT,
	timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS world_state (
	id			SERIAL		PRIMARY KEY,
	planetname	TEXT  DEFAULT "mars",
	lookingat 	TEXT  DEFAULT "",
	pressure 	FLOAT DEFAULT 0.0,
	temperature FLOAT DEFAULT 0.0,
	gravity FLOAT DEFAULT 0.0,
	n2Level FLOAT DEFAULT 0.0,
	co2Level FLOAT DEFAULT 0.0,
	o2Level FLOAT DEFAULT 0.0,
	isdaytime	BOOLEAN DEFAULT TRUE NOT NULL,
	islighton	BOOLEAN DEFAULT TRUE NOT NULL,
	isdrillon	BOOLEAN DEFAULT TRUE NOT NULL,
	settings	TEXT DEFAULT "",
	action		TEXT DEFAULT "",
	timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);
