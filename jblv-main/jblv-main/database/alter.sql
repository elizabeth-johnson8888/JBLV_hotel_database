-----------------------------------------------------
-- Primary Keys
------------------------------------------------------
ALTER TABLE hotel
    ADD PRIMARY KEY (hotel_id);

ALTER TABLE hotel_phones
    ADD PRIMARY KEY (hotel_id, name);

ALTER TABLE seasons
    ADD PRIMARY KEY (season_id);

ALTER TABLE employee
    ADD PRIMARY KEY (employee_id);

ALTER TABLE admin
    ADD PRIMARY KEY (employee_id, department_id);

ALTER TABLE cleaning
    ADD PRIMARY KEY (employee_id, department_id);

ALTER TABLE cleaning_schedule
    ADD PRIMARY KEY (schedule_id);

ALTER TABLE room_type
    ADD PRIMARY KEY (type_id, hotel_id);

ALTER TABLE room
    ADD PRIMARY KEY (room_num);

ALTER TABLE reservation
    ADD PRIMARY KEY (reservation_id);

-- ALTER TABLE occupant
--     ADD PRIMARY KEY (reservation_id);

ALTER TABLE guest
    ADD PRIMARY KEY (guest_id);

ALTER TABLE guest_category
    ADD PRIMARY KEY (hotel_id, guest_id);

ALTER TABLE bill
    ADD PRIMARY KEY (guest_id, bill_id);

ALTER TABLE review
    ADD PRIMARY KEY (guest_id, display_name, date);

ALTER TABLE service
    ADD PRIMARY KEY (service_id);

ALTER TABLE spa_service
    ADD PRIMARY KEY (id, service_id, hotel_id);

ALTER TABLE hotel_features
    ADD PRIMARY KEY (hotel_id, name);

ALTER TABLE room_features
    ADD PRIMARY KEY (type_id, name, hotel_id);

--------------------------------------------------------------
-- Foreign Keys
---------------------------------------------------------------
ALTER TABLE seasons
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE day_discount
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE hotel_phones
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE employee
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE admin
    ADD FOREIGN KEY (employee_id)
    REFERENCES employee (employee_id);

ALTER TABLE cleaning
    ADD FOREIGN KEY (employee_id)
    REFERENCES employee (employee_id);

ALTER TABLE cleaning
    ADD FOREIGN KEY (schedule_id)
    REFERENCES cleaning_schedule (schedule_id);

ALTER TABLE room_type
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE room
    ADD FOREIGN KEY (type_id, hotel_id)
    REFERENCES room_type (type_id, hotel_id);

ALTER TABLE reservation
    ADD FOREIGN KEY (type_id, hotel_id)
    REFERENCES room_type (type_id, hotel_id);

ALTER TABLE reservation
    ADD FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id);

ALTER TABLE reservation
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE occupant
    ADD FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id);

ALTER TABLE guest_category
    ADD FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id);

ALTER TABLE bill
    ADD FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id);


ALTER TABLE bill
    ADD FOREIGN KEY (reservation_id)
    REFERENCES reservation (reservation_id);


ALTER TABLE review
    ADD FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id);

-- ALTER TABLE service
--     ADD FOREIGN KEY (bill_id)
--     REFERENCES bill (bill_id);

ALTER TABLE service
    ADD FOREIGN KEY (guest_id)
    REFERENCES guest (guest_id);

ALTER TABLE service
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE spa_service
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE spa_service
    ADD FOREIGN KEY (service_id)
    REFERENCES service (service_id);

ALTER TABLE hotel_features
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);

ALTER TABLE room_features
    ADD FOREIGN KEY (type_id, hotel_id)
    REFERENCES room_type (type_id, hotel_id);
	
ALTER TABLE room_features
    ADD FOREIGN KEY (hotel_id)
    REFERENCES hotel (hotel_id);
--------------------------------------------------------------------------
-- Indexes
--------------------------------------------------------------------------
CREATE INDEX guest_index ON guest (guest_id);
CREATE INDEX reservation_index ON occupant (reservation_id);

CREATE INDEX bill_index ON bill (guest_id);

CREATE INDEX clean_index ON room (is_clean);


--------------------------------------------------------------------------
-- Alter table owners
--------------------------------------------------------------------------
ALTER TABLE hotel OWNER TO jblv;
ALTER TABLE hotel_phones OWNER TO jblv;
ALTER TABLE seasons OWNER TO jblv;
ALTER TABLE employee OWNER TO jblv;
ALTER TABLE admin OWNER TO jblv;
ALTER TABLE cleaning OWNER TO jblv;
ALTER TABLE cleaning_schedule OWNER TO jblv;
ALTER TABLE room_type OWNER TO jblv;
ALTER TABLE room OWNER TO jblv;
ALTER TABLE reservation OWNER TO jblv;
ALTER TABLE occupant OWNER TO jblv;
ALTER TABLE guest OWNER TO jblv;
ALTER TABLE guest_category OWNER TO jblv;
ALTER TABLE bill OWNER TO jblv;
ALTER TABLE review OWNER TO jblv;
ALTER TABLE service OWNER TO jblv;
ALTER TABLE hotel_features OWNER TO jblv;
ALTER TABLE room_features OWNER TO jblv;
ALTER TABLE day_discount OWNER TO jblv;
ALTER TABLE spa_service OWNER TO jblv;
