-- Creating MOVIES table
CREATE TABLE IF NOT EXISTS movies (
    movie_id TEXT PRIMARY KEY NOT NULL UNIQUE,
    title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    genre TEXT,
    CONSTRAINT unique_movie UNIQUE (title, release_year)
);

-- Creating ACTORS table
CREATE TABLE IF NOT EXISTS actors (
    actor_id TEXT PRIMARY KEY NOT NULL UNIQUE,
    name TEXT NOT NULL,
    birth_year INTEGER NOT NULL,
    CONSTRAINT unique_actor UNIQUE (name, birth_year)
);

-- Creating MOVIE_CAST table
CREATE TABLE IF NOT EXISTS movie_cast (
    movie_cast_id TEXT PRIMARY KEY NOT NULL UNIQUE,
    movie_id TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    CONSTRAINT cast_movie_ref FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    CONSTRAINT cast_actor_ref FOREIGN KEY (actor_id) REFERENCES actors(actor_id),
    CONSTRAINT actor_in_movie UNIQUE (actor_id, movie_id)
);

-- Populating MOVIES table with values
INSERT OR IGNORE INTO movies (movie_id, title, release_year, genre)
    VALUES
    (uuid(), 'Inception', 2010, 'Sci-Fi'),
    (uuid(), 'The Dark Knight', 2008, 'Action'),
    (uuid(), 'Interstellar', 2014, 'Sci-Fi'),
    (uuid(), 'The Revenant', 2015, 'Drama'),
    (uuid(), 'Titanic', 1997, 'Romance'),
    (uuid(), 'Shutter Island', 2010, 'Thriller'),
    (uuid(), 'Django Unchained', 2012, 'Western'),
    (uuid(), 'The Wolf of Wall Street', 2013, 'Comedy'),
    (uuid(), 'Mad Max: Fury Road', 2015, 'Action'),
    (uuid(), 'The Martian', 2015, 'Sci-Fi');

-- Populating ACTORS table with values
INSERT OR IGNORE INTO actors (actor_id, name, birth_year)
    VALUES
    (uuid(), 'Leonardo DiCaprio', 1974),
    (uuid(), 'Joseph Gordon-Levitt', 1981),
    (uuid(), 'Christian Bale', 1974),
    (uuid(), 'Heath Ledger', 1979),
    (uuid(), 'Matthew McConaughey', 1969),
    (uuid(), 'Anne Hathaway', 1982),
    (uuid(), 'Tom Hardy', 1977),
    (uuid(), 'Domhnall Gleeson', 1983),
    (uuid(), 'Kate Winslet', 1975),
    (uuid(), 'Billy Zane', 1966),
    (uuid(), 'Mark Ruffalo', 1967),
    (uuid(), 'Ben Kingsley', 1943),
    (uuid(), 'Jamie Foxx', 1967),
    (uuid(), 'Christoph Waltz', 1956),
    (uuid(), 'Jonah Hill', 1983),
    (uuid(), 'Margot Robbie', 1990),
    (uuid(), 'Charlize Theron', 1975),
    (uuid(), 'Nicholas Hoult', 1989),
    (uuid(), 'Matt Damon', 1970),
    (uuid(), 'Jessica Chastain', 1977);

-- Populating MOVIE_CAST table with movies and cast data
INSERT OR IGNORE INTO movie_cast (movie_cast_id, movie_id, actor_id)
    VALUES
    -- Inception (2010)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Inception'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Inception'),
             (SELECT actor_id FROM actors WHERE name = 'Joseph Gordon-Levitt')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Inception'),
             (SELECT actor_id FROM actors WHERE name = 'Tom Hardy')),

    -- The Dark Knight (2008)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Dark Knight'),
             (SELECT actor_id FROM actors WHERE name = 'Christian Bale')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Dark Knight'),
             (SELECT actor_id FROM actors WHERE name = 'Heath Ledger')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Dark Knight'),
             (SELECT actor_id FROM actors WHERE name = 'Tom Hardy')),

    -- Interstellar (2014)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Interstellar'),
             (SELECT actor_id FROM actors WHERE name = 'Matthew McConaughey')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Interstellar'),
             (SELECT actor_id FROM actors WHERE name = 'Anne Hathaway')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Interstellar'),
             (SELECT actor_id FROM actors WHERE name = 'Matt Damon')),

    -- The Revenant (2015)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Revenant'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Revenant'),
             (SELECT actor_id FROM actors WHERE name = 'Tom Hardy')),

    -- Titanic (1997)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Titanic'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Titanic'),
             (SELECT actor_id FROM actors WHERE name = 'Kate Winslet')),

    -- Shutter Island (2010)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Shutter Island'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Shutter Island'),
             (SELECT actor_id FROM actors WHERE name = 'Mark Ruffalo')),

    -- Django Unchained (2012)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Django Unchained'),
             (SELECT actor_id FROM actors WHERE name = 'Jamie Foxx')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Django Unchained'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Django Unchained'),
             (SELECT actor_id FROM actors WHERE name = 'Christoph Waltz')),

    -- The Wolf of Wall Street (2013)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Wolf of Wall Street'),
             (SELECT actor_id FROM actors WHERE name = 'Leonardo DiCaprio')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Wolf of Wall Street'),
             (SELECT actor_id FROM actors WHERE name = 'Jonah Hill')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Wolf of Wall Street'),
             (SELECT actor_id FROM actors WHERE name = 'Margot Robbie')),

    -- Mad Max: Fury Road (2015)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Mad Max: Fury Road'),
             (SELECT actor_id FROM actors WHERE name = 'Tom Hardy')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Mad Max: Fury Road'),
             (SELECT actor_id FROM actors WHERE name = 'Charlize Theron')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'Mad Max: Fury Road'),
             (SELECT actor_id FROM actors WHERE name = 'Nicholas Hoult')),

    -- The Martian (2015)
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Martian'),
             (SELECT actor_id FROM actors WHERE name = 'Matt Damon')),
    (uuid(), (SELECT movie_id FROM movies WHERE title = 'The Martian'),
             (SELECT actor_id FROM actors WHERE name = 'Jessica Chastain'))
