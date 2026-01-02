CREATE TABLE IF NOT EXISTS users (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "login" TEXT,
    "password" TEXT
);
CREATE TABLE IF NOT EXISTS tasks (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INT,
    "name" TEXT,
    "text" TEXT,
    "state" TEXT,
    "date" TIMESTAMP
);