-- Insert sample estate agent data --

INSERT INTO EstateAgent (name, address, username, password)
VALUES ('John Doe', 'Vogt-Kölln-Straße 30, Hamburg', 'john.doe', 'secure123');

INSERT INTO EstateAgent (name, address, username, password)
VALUES ('Jane Smith', 'Grindelallee 117, Hamburg', 'jane.smith', 'agent456');

-- Insert sample estates --
INSERT INTO Estate (city, postal_code, street, street_number, square_area, agent_id)
VALUES ('Hamburg', '20146', 'Universitätsstraße', '1', 75.50, 1);

INSERT INTO Estate (city, postal_code, street, street_number, square_area, agent_id)
VALUES ('Hamburg', '20148', 'Grindelallee', '23', 120.75, 1);

INSERT INTO Estate (city, postal_code, street, street_number, square_area, agent_id)
VALUES ('Hamburg', '20144', 'Schlüterstraße', '12', 150.00, 2);

INSERT INTO Estate (city, postal_code, street, street_number, square_area, agent_id)
VALUES ('Hamburg', '20354', 'Rothenbaumchaussee', '45', 200.00, 2);

-- Insert sample apartments
INSERT INTO Apartment (estate_id, floor_number, rent, rooms, balcony, built_in_kitchen)
VALUES (1, 3, 1200.00, 2, true, true);

INSERT INTO Apartment (estate_id, floor_number, rent, rooms, balcony, built_in_kitchen)
VALUES (2, 1, 1500.00, 3, false, true);

-- Insert sample houses
INSERT INTO House (estate_id, floors, price, garden)
VALUES (3, 2, 500000.00, true);

INSERT INTO House (estate_id, floors, price, garden)
VALUES (4, 3, 750000.00, true);

-- Insert sample persons (potential tenants/buyers)
INSERT INTO Person (first_name, name, address)
VALUES ('Marie', 'Weber', 'Schlüterstraße 28, Hamburg');

INSERT INTO Person (first_name, name, address)
VALUES ('Thomas', 'Mueller', 'Grindelhof 15, Hamburg');

INSERT INTO Person (first_name, name, address)
VALUES ('Sarah', 'Schmidt', 'Bundesstraße 45, Hamburg');

INSERT INTO Person (first_name, name, address)
VALUES ('Michael', 'Fischer', 'Moorweidenstraße 18, Hamburg');

-- Insert base contracts
INSERT INTO Contract (person_id, date, place)
VALUES (1, '2024-01-15', 'Hamburg');

INSERT INTO Contract (person_id, date, place)
VALUES (2, '2024-02-01', 'Hamburg');

INSERT INTO Contract (person_id, date, place)
VALUES (3, '2024-03-10', 'Hamburg');

INSERT INTO Contract (person_id, date, place)
VALUES (4, '2024-03-15', 'Hamburg');

-- Insert tenancy contracts
INSERT INTO TenancyContract (contract_no, estate_id, start_date, duration, additional_costs)
VALUES (1, 1, '2024-02-01', 24, 200.00);

INSERT INTO TenancyContract (contract_no, estate_id, start_date, duration, additional_costs)
VALUES (2, 2, '2024-03-01', 12, 250.00);

-- Insert purchase contracts
INSERT INTO PurchaseContract (contact_no, estate_id, number_of_installments, interest_rate)
VALUES (3, 1, 360, 3.5);

INSERT INTO PurchaseContract (contact_no, estate_id, number_of_installments, interest_rate)
VALUES (4, 2, 240, 3.8);


