-- DO NOT ADD KEYS YET, ADD IN ALTER.SQL
-- Represents a hotel
DROP TABLE IF EXISTS hotel CASCADE;
CREATE TABLE hotel (
    hotel_id INT UNIQUE,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
    -- day_discount DECIMAL NOT NULL
	-- season_name VARCHAR(255) NOT NULL because there are 3 seasons per hotel
);


-- Represents a phone numbers associated with a hotel location
DROP TABLE IF EXISTS hotel_phones CASCADE;
CREATE TABLE hotel_phones (
    hotel_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    number VARCHAR(225) NOT NULL
);

-- Represents the seasons of the year
DROP TABLE IF EXISTS seasons CASCADE;
CREATE TABLE seasons (
    -- hotels have multiple seasons so the season name will not be unique
    season_id INT UNIQUE,
    season_name VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
	discount DECIMAL NOT NULL,
    hotel_id INT NOT NULL
);

-- Represents an employee hired at the hotel
DROP TABLE IF EXISTS employee CASCADE;
CREATE TABLE employee (
    employee_id INT UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
	hotel_id INT NOT NULL
);

-- Represents the admin employee department
DROP TABLE IF EXISTS admin CASCADE;
CREATE TABLE admin (
    employee_id INT UNIQUE NOT NULL,
    department_id INT NOT NULL
);

-- Represents the cleaning employee department
DROP TABLE IF EXISTS cleaning CASCADE;
CREATE TABLE cleaning (
    employee_id INT UNIQUE NOT NULL,
    department_id INT NOT NULL,
    schedule_id INT NOT NULL
);

-- Represents the cleaning schedule associated with the hotels cleaning staff
DROP TABLE IF EXISTS cleaning_schedule CASCADE;
CREATE TABLE cleaning_schedule (
    schedule_id INT NOT NULL,
    date DATE NOT NULL
);

-- Represents room types within a hotel
DROP TABLE IF EXISTS room_type CASCADE;
CREATE TABLE room_type (
    type_id VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL,
    capacity INT NOT NULL,
    sq_ft INT NOT NULL,
	hotel_id INT NOT NULL
);

-- Represents the rooms that exist within a hotel
DROP TABLE IF EXISTS room CASCADE;
CREATE TABLE room (
    room_num INT,
    floor_num INT NOT NULL,
    is_clean BOOLEAN NOT NULL,
	type_id VARCHAR(255) NOT NULL,
	is_occupied BOOLEAN NOT NULL,
	hotel_id INT NOT NULL
);

-- Represents a reservation made by a the hotel
DROP TABLE IF EXISTS reservation CASCADE;
CREATE TABLE reservation (
    reservation_id INT,
    guest_id INT NOT NULL,
    checkin_date TIMESTAMP NOT NULL,
    checkout_date TIMESTAMP NOT NULL,
    room_num INT NULL,
	type_id VARCHAR(255) NOT NULL,
	actual_checkin TIMESTAMP NULL,
	actual_checkout TIMESTAMP NULL,
    hotel_id INT NOT NULL
);

-- Represents the guest present in a room per reservation, not including the booking guest
DROP TABLE IF EXISTS occupant CASCADE;
CREATE TABLE occupant (
    reservation_id INT NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- Represents the guest that booked the reservation
DROP TABLE IF EXISTS guest CASCADE;
CREATE TABLE guest (
    guest_id INT UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    mobile_phone VARCHAR(255) NOT NULL,
    home_phone VARCHAR(255) NOT NULL,
    id_type VARCHAR(255) NOT NULL,
    id_number INT NOT NULL
);

-- Represents a category a guest can belong in
DROP TABLE IF EXISTS guest_category CASCADE;
CREATE TABLE guest_category (
    hotel_id INT NOT NULL,
    guest_id INT NULL,
    name VARCHAR(255) NOT NULL,
    discount DECIMAL NOT NULL
);

-- Represents the bill a guest recieves after a reservation
-- past bills can be found here as well
DROP TABLE IF EXISTS bill CASCADE;
CREATE TABLE bill (
    guest_id INT NOT NULL,
    bill_id SERIAL,
    total DECIMAL NOT NULL,
    reservation_id INT NOT NULL
);

-- Represents a review that a guest can leave for the hotel
DROP TABLE IF EXISTS review CASCADE;
CREATE TABLE review (
    guest_id INT NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(255) NOT NULL,
    date DATE NOT NULL
);

-- Represents a service that guest ordered through the hotel
-- For example: room service, extra cleaning service, spa service,
DROP TABLE IF EXISTS service CASCADE;
CREATE TABLE service (
    service_id INT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL,
    guest_id INT NOT NULL,
	hotel_id INT NOT NULL
);

DROP TABLE IF EXISTS spa_service CASCADE;
CREATE TABLE spa_service (
    id INT,
    service_id INT NOT NULL,
    service_cat VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL,
	hotel_id INT NOT NULL
);

-- Represents features available in the hotel
-- For example: spa, pool, breakfast, gym, etc.
DROP TABLE IF EXISTS hotel_features CASCADE;
CREATE TABLE hotel_features (
    hotel_id INT NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- Represents features available from the rooms in the hotel
-- For example: kitchenette, etc.
DROP TABLE IF EXISTS room_features CASCADE;
CREATE TABLE room_features (
    type_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    hotel_id INT NOT NULL
);

DROP TABLE IF EXISTS day_discount CASCADE;
CREATE TABLE day_discount (
    weekday INT NOT NULL,
    discount DECIMAL NOT NULL,
    hotel_id INT NOT NULL
);
