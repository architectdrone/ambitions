CREATE TABLE ambitions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
);

CREATE TABLE virtues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    ambition INTEGER,
    FOREIGN KEY(ambition) REFERENCES ambitions(id)
);

CREATE TABLE finite_projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent INTEGER,
    infinite_project INTEGER,
    FOREIGN KEY(parent) REFERENCES finite_projects(id),
    FOREIGN KEY(infinite_project) REFERENCES infinite_projects(id)
);

CREATE TABLE infinite_projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    parent INTEGER,
    FOREIGN KEY(parent) REFERENCES finite_projects(id)
);

CREATE TABLE tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    finite_project INTEGER,
    parent INTEGER,
    FOREIGN KEY(finite_project) REFERENCES finite_projects(id),
    FOREIGN KEY(parent) REFERENCES tasks(id)
);

CREATE TABLE positives(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    infinite_project INTEGER,
    FOREIGN KEY(infinite_project) REFERENCES infinite_projects(id)
);

CREATE TABLE negatives(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    infinite_project INTEGER,
    FOREIGN KEY(infinite_project) REFERENCES infinite_projects(id)
);

CREATE TABLE ambition_ambition(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent INTEGER,
    child INTEGER,
    FOREIGN KEY(parent) REFERENCES ambitions(id),
    FOREIGN KEY(child) REFERENCES ambitions(id)
);

CREATE TABLE virtue_finite_project(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    virtue INTEGER,
    finite_project INTEGER,
    FOREIGN KEY(virtue) REFERENCES virtues(id),
    FOREIGN key(finite_project) REFERENCES finite_projects(id)
);

CREATE TABLE virtue_infinite_project(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    virtue INTEGER,
    infinite_project INTEGER,
    FOREIGN KEY(virtue) REFERENCES virtues(id),
    FOREIGN key(infinite_project) REFERENCES infinite_projects(id)
);