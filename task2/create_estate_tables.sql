

CREATE TABLE estate_agent (
    agent_id         SERIAL PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    address          VARCHAR(255),
    login            VARCHAR(80)  UNIQUE NOT NULL,
    password         VARCHAR(120) NOT NULL
);

CREATE TABLE person (
    person_id   SERIAL PRIMARY KEY,
    first_name  VARCHAR(60),
    name        VARCHAR(60)  NOT NULL,
    address     VARCHAR(255)
);


CREATE TABLE estate (
    estate_id     SERIAL PRIMARY KEY,
    city          VARCHAR(60),
    postal_code   VARCHAR(15),
    street        VARCHAR(80),
    street_number VARCHAR(15),
    square_area   NUMERIC(10,2) CHECK (square_area >= 0),


    agent_id      INT NOT NULL
        REFERENCES estate_agent (agent_id)
        ON DELETE RESTRICT
);

CREATE TABLE apartment (
    estate_id         INT PRIMARY KEY
        REFERENCES estate (estate_id)
        ON DELETE CASCADE,
    floor             INT,
    rent              NUMERIC(12,2) CHECK (rent >= 0),
    rooms             INT,
    balcony           BOOLEAN DEFAULT FALSE,
    built_in_kitchen  BOOLEAN DEFAULT FALSE
);

CREATE TABLE house (
    estate_id  INT PRIMARY KEY
        REFERENCES estate (estate_id)
        ON DELETE CASCADE,
    floors     INT,
    price      NUMERIC(14,2) CHECK (price >= 0),
    garden     BOOLEAN DEFAULT FALSE
);


CREATE TABLE contract (
    contract_no   SERIAL PRIMARY KEY,
    contract_date DATE    NOT NULL,
    place         VARCHAR(120)
);



CREATE TABLE tenancy_contract (
    contract_no       INT PRIMARY KEY
        REFERENCES contract (contract_no)
        ON DELETE CASCADE,
    start_date        DATE NOT NULL,
    duration          INT  CHECK (duration > 0),          
    additional_costs  NUMERIC(12,2),

    person_id    INT NOT NULL
        REFERENCES person (person_id)
        ON DELETE RESTRICT,
    apartment_id INT NOT NULL
        REFERENCES apartment (estate_id)
        ON DELETE RESTRICT,


    UNIQUE (apartment_id)
);


CREATE TABLE purchase_contract (
    contract_no         INT PRIMARY KEY
        REFERENCES contract (contract_no)
        ON DELETE CASCADE,
    no_of_installments  INT     CHECK (no_of_installments > 0),
    interest_rate       NUMERIC(5,2),

    person_id  INT NOT NULL
        REFERENCES person (person_id)
        ON DELETE RESTRICT,
    house_id   INT NOT NULL
        REFERENCES house (estate_id)
        ON DELETE RESTRICT,

    UNIQUE (house_id)
);

