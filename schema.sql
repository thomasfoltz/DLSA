DROP TABLE IF EXISTS stocks;

CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ticker TEXT NOT NULL,
    quantity INTEGER NOT NULL
);