CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    fullname TEXT NOT NULL,
    "group" TEXT NOT NULL,
    CONSTRAINT uq_name_group UNIQUE (fullname, "group")
);

CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    "date" DATE,
    grade INTEGER NOT NULL,

    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);