CREATE TABLE IF NOT EXISTS alexa_response (
	id			SERIAL		PRIMARY KEY,
	link	TEXT,
	settings	TEXT,
	timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS world_state (
	id			SERIAL		PRIMARY KEY,
	planetname	TEXT,
	lookingat 	TEXT,
	pressure 	FLOAT,
	temperature FLOAT,
	isdaytime	BOOLEAN DEFAULT TRUE NOT NULL,
	islighton	BOOLEAN DEFAULT TRUE NOT NULL,
	isdrillon	BOOLEAN DEFAULT TRUE NOT NULL,
	settings	TEXT,
	timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);
