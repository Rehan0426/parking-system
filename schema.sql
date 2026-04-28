CREATE TABLE IF NOT EXISTS slots (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plate TEXT NOT NULL,
    slot_id INTEGER,
    slot_number TEXT,
    type TEXT,
    owner TEXT,
    phone TEXT,
    entry_time TEXT,
    exit_time TEXT,
    hours INTEGER,
    amount INTEGER,
    FOREIGN KEY (slot_id) REFERENCES slots(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER,
    plate TEXT,
    amount INTEGER,
    method TEXT,
    time TEXT,
    FOREIGN KEY (record_id) REFERENCES records(id)
);