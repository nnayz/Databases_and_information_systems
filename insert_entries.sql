-- Create the table 'demo' if not exists --

CREATE TABLE IF NOT EXISTS demo(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Insert data into the demo table --

INSERT INTO demo (username, password, email) VALUES ('nayz', 'Hello123', 'nayz@gmail.com');
INSERT INTO demo (username, password, email) VALUES ('john', 'Hello123', 'john@gmail.com');
INSERT INTO demo (username, password, email) VALUES ('jane', 'Hello123', 'jane@gmail.com');
INSERT INTO demo (username, password, email) VALUES ('jim', 'Hello123', 'jim@gmail.com');
INSERT INTO demo (username, password, email) VALUES ('jill', 'Hello123', 'jill@gmail.com');
INSERT INTO demo (username, password, email) VALUES ('jeff', 'Hello123', 'jeff@gmail.com');
