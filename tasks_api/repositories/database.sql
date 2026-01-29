CREATE TABLE IF NOT EXISTS users (
    "id" SERIAL PRIMARY KEY,
    "login" TEXT,
    "password" TEXT
);
CREATE TABLE IF NOT EXISTS tasks (
    "id" SERIAL PRIMARY KEY,
    "user_id" INT,
    "name" TEXT,
    "text" TEXT,
    "state" TEXT,
    "date" TIMESTAMP
);