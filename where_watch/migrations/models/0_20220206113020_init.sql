-- upgrade --
CREATE TABLE IF NOT EXISTS "series" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL UNIQUE,
    "title_eng" VARCHAR(255) NOT NULL UNIQUE,
    "poster" VARCHAR(255) NOT NULL,
    "premiere_date" DATE NOT NULL,
    "update_date" DATE NOT NULL
);
CREATE TABLE IF NOT EXISTS "site" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(60) NOT NULL UNIQUE,
    "url" VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "sitelink" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "link" VARCHAR(255) NOT NULL,
    "site_id" INT NOT NULL REFERENCES "site" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "series_sitelink" (
    "series_id" INT NOT NULL REFERENCES "series" ("id") ON DELETE CASCADE,
    "sitelink_id" INT NOT NULL REFERENCES "sitelink" ("id") ON DELETE CASCADE
);
