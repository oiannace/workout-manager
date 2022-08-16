DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS exercise_stats;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE exercise_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  exercise_name TEXT NOT NULL,
  num_sets INTEGER NOT NULL,
  num_reps INTEGER NOT NULL,
  weight INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE workout (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  exercise_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL,
  FOREIGN KEY (exercise_id) REFERENCES exercise_stats (id)
  FOREIGN KEY (user_id) REFERENCES user (id)
);