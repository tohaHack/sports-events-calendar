-- drop tables if they exist
DROP TABLE IF EXISTS sport;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS venue;


-- create venues table
CREATE TABLE venue (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL
);

-- create sports table
CREATE TABLE sport (
    sport_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each sport
    name VARCHAR(100) NOT NULL UNIQUE -- name of the sport
);

-- create teams table
CREATE TABLE team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each team
    name VARCHAR(100) NOT NULL -- name of the team
);

-- central events table
CREATE TABLE event (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, -- unique identifier for each event
    event_date DATETIME NOT NULL, -- date and time of the event
    description TEXT, -- description of the event
    _sport_id INTEGER NOT NULL, -- foreign key referencing sports table
    _home_team_id INTEGER NOT NULL, -- foreign key referencing first team
    _away_team_id INTEGER NOT NULL, -- foreign key referencing second team
    _venue_id INTEGER NOT NULL,

    -- establish foreign key relationships
    FOREIGN KEY (_sport_id) REFERENCES sport(sport_id) ON DELETE CASCADE,
    FOREIGN KEY (_home_team_id) REFERENCES team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (_away_team_id) REFERENCES team(team_id) ON DELETE CASCADE,
    FOREIGN KEY (_venue_id) REFERENCES venue(venue_id) ON DELETE CASCADE
);