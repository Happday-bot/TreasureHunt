import sqlite3

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create tables
cursor.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS location_summary (
    user_id INTEGER UNIQUE NOT NULL,
    location_count INTEGER NOT NULL,
    hint_count INTEGER NOT NULL CHECK(hint_count < 4),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_locations (
    user_id INTEGER UNIQUE NOT NULL,
    location1 TEXT, location2 TEXT, location3 TEXT,
    location4 TEXT, location5 TEXT, location6 TEXT,
    location7 TEXT, location8 TEXT, location9 TEXT,
    location10 TEXT, location11 TEXT, location12 TEXT, location13 TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS location_answers (
    location_name TEXT PRIMARY KEY,
    possible_answers TEXT NOT NULL,
    q1 TEXT NOT NULL,
    q2 TEXT NOT NULL,
    q3 TEXT NOT NULL,
    q4 TEXT NOT NULL
);
""")

# Insert users
users_data = [
    (123, 'user1', 'pass1'),
    (234, 'user2', 'pass2'),
    (567, 'user3', 'pass3')
]
cursor.executemany("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", users_data)

# Insert location_summary
location_summary_data = [
    (123, 1, 3),
    (234, 1, 3),
    (567, 1, 3)
]
cursor.executemany("INSERT INTO location_summary (user_id, location_count, hint_count) VALUES (?, ?, ?)", location_summary_data)

# Insert user_locations
user_locations_data = [
    (123, 'London', 'Tokyo', 'Paris', 'Sydney', None, None, None, None, None, None, None, None, None),
    (234, 'London', 'Paris', 'Tokyo', 'Sydney', None, None, None, None, None, None, None, None, None),
    (567, 'Dubai', 'Cairo', 'Moscow', 'Delhi', None, None, None, None, None, None, None, None, None)
]
cursor.executemany("INSERT INTO user_locations (user_id, location1, location2, location3, location4, location5, location6, location7, location8, location9, location10, location11, location12, location13) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user_locations_data)

# Insert location_answers
location_answers_data = [
    ('Paris', 'Eiffel Tower, Louvre, Seine River', 'What is the capital of France?', 'Where is the Eiffel Tower?', 'Which city has the Louvre?', 'Which city is known as the City of Light?'),
    ('London', 'Big Ben, Thames River, Buckingham Palace', 'What is the capital of the UK?', 'Where is Big Ben?', 'Which city has Buckingham Palace?', 'Which city is on the Thames River?'),
    ('Tokyo', 'Mount Fuji, Shibuya Crossing, Akihabara', 'What is the capital of Japan?', 'Where is Mount Fuji?', 'Which city has Shibuya Crossing?', 'Which city is famous for anime and technology?')
]
cursor.executemany("INSERT INTO location_answers (location_name, possible_answers, q1, q2, q3, q4) VALUES (?, ?, ?, ?, ?, ?)", location_answers_data)

# Commit changes and close connection
conn.commit()
conn.close()
