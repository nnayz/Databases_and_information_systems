-- Populate estate_agent table
INSERT INTO estate_agent (name, address, login, password) VALUES 
('John Smith', '123 Main St, Hamburg', 'jsmith', 'password123'),
('Emma Weber', '456 Oak Ave, Hamburg', 'eweber', 'secure456'),
('Michael Braun', '789 Pine Rd, Berlin', 'mbraun', 'agent789'),
('Sophia Klein', '321 Elm Blvd, Munich', 'sklein', 'realtor321');

-- Populate person table
INSERT INTO person (first_name, name, address) VALUES 
('Thomas', 'Mueller', '111 River St, Hamburg'),
('Anna', 'Schmidt', '222 Mountain Ave, Berlin'),
('Paul', 'Wagner', '333 Forest Rd, Munich'),
('Laura', 'Fischer', '444 Lake Blvd, Frankfurt'),
('Max', 'Becker', '555 Hill St, Cologne'),
('Julia', 'Hoffmann', '666 Valley Rd, Dresden');

-- Populate estate table
INSERT INTO estate (city, postal_code, street, street_number, square_area, agent_id) VALUES 
('Hamburg', '20095', 'Hafenstrasse', '10', 75.5, 1),
('Hamburg', '22085', 'Mozartstrasse', '25', 120.0, 1),
('Berlin', '10115', 'Friedrichstrasse', '100', 60.0, 2),
('Munich', '80331', 'Marienplatz', '8', 95.0, 3),
('Berlin', '10117', 'Unter den Linden', '17', 150.0, 2),
('Hamburg', '22083', 'Bachstrasse', '12', 80.0, 4);

-- Populate apartment table
INSERT INTO apartment (estate_id, floor, rent, rooms, balcony, built_in_kitchen) VALUES 
(1, 3, 1200.00, 2, TRUE, TRUE),
(3, 5, 950.00, 1, FALSE, TRUE),
(4, 2, 1500.00, 3, TRUE, FALSE);

-- Populate house table
INSERT INTO house (estate_id, floors, price, garden) VALUES 
(2, 2, 450000.00, TRUE),
(5, 3, 750000.00, TRUE),
(6, 2, 350000.00, FALSE);

-- Populate contract table
INSERT INTO contract (contract_date, place) VALUES 
('2023-06-15', 'Hamburg'),
('2023-07-20', 'Berlin'),
('2023-08-10', 'Munich'),
('2023-09-05', 'Berlin'),
('2023-10-12', 'Hamburg');

-- Populate tenancy_contract table
INSERT INTO tenancy_contract (contract_no, start_date, duration, additional_costs, person_id, apartment_id) VALUES 
(1, '2023-07-01', 24, 200.00, 1, 16),
(2, '2023-08-01', 12, 150.00, 2, 18);

-- Populate purchase_contract table
INSERT INTO purchase_contract (contract_no, no_of_installments, interest_rate, person_id, house_id) VALUES 
(3, 240, 3.5, 3, 17),
(4, 360, 2.8, 4, 20),
(5, 180, 3.2, 5, 21); 