-- Flask To-Do Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS todos;
DROP TABLE IF EXISTS users;

-- Users
CREATE TABLE users (
  user_id bigserial PRIMARY KEY,
  email varchar(100) UNIQUE NOT NULL ,
  password varchar(100) NOT NULL,
  name varchar(100) NOT NULL
);

-- To-Do Items
CREATE TABLE todos (
    id bigserial PRIMARY KEY,
    description varchar(140) NOT NULL,
    completed boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    users_id bigint REFERENCES users(user_id)
);
