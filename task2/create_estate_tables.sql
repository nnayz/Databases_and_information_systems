-- create estate tables --

-- Create the estateAgent table --
CREATE TABLE IF NOT EXISTS EstateAgent (
    agent_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create the estate table --
CREATE TABLE IF NOT EXISTS Estate (
    estate_id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    street VARCHAR(255) NOT NULL,
    street_number VARCHAR(20) NOT NULL,
    square_area DECIMAL(10, 2),
    agent_id INTEGER NOT NULL,
    FOREIGN KEY (agent_id) REFERENCES EstateAgent(agent_id)
);

-- CREATE the apartments table --
CREATE TABLE IF NOT EXISTS Apartment (
    apartment_id SERIAL PRIMARY KEY,
    estate_id INTEGER NOT NULL,
    floor_number INTEGER NOT NULL,
    rent DECIMAL(10, 2),
    rooms INTEGER,
    balcony BOOLEAN,
    built_in_kitchen BOOLEAN,
    FOREIGN KEY (estate_id) REFERENCES Estate(estate_id)
);

-- Create the house table --
CREATE TABLE IF NOT EXISTS House (
    house_id SERIAL PRIMARY KEY,
    estate_id INTEGER NOT NULL,
    floors INTEGER NOT NULL,
    price DECIMAL(10, 2),
    garden BOOLEAN,
    FOREIGN KEY (estate_id) REFERENCES Estate(estate_id)
);

-- Create the Person table --
CREATE TABLE IF NOT EXISTS Person (
    person_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255)
);

-- Create the Contract table --
CREATE TABLE IF NOT EXISTS Contract (
    contract_no SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,
    date DATE NOT NULL,
    place VARCHAR(255),
    FOREIGN KEY (person_id) REFERENCES Person(person_id)
);


-- Create the TenancyContract table --
CREATE TABLE IF NOT EXISTS TenancyContract (
    contract_no INTEGER NOT NULL,
    estate_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    duration INTEGER NOT NULL,
    additional_costs DECIMAL(10, 2),
    FOREIGN KEY (estate_id) REFERENCES Apartment(apartment_id),
    FOREIGN KEY (contract_no) REFERENCES Contract(contract_no)
);

-- Create the PurchaseContract table --
CREATE TABLE IF NOT EXISTS PurchaseContract (
    contact_no INTEGER NOT NULL,
    estate_id INTEGER NOT NULL,
    number_of_installments INTEGER,
    interest_rate DECIMAL(5, 2),
    FOREIGN KEY (estate_id) REFERENCES House(house_id),
    FOREIGN KEY (contact_no) REFERENCES Contract(contract_no)
);






