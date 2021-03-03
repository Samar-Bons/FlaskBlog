/* A simple sql script to init a new database for our application */

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (

    /* We will only be concerned with adding a title and content by the user 
        since 'id' and 'created' are expected to autogenerate */
        
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
