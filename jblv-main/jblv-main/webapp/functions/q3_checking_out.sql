-- Query 3
--   Two nights have passed, and Mr. and Mrs. Smith are ready to check out.
--   Write a query to generate the billing statement for the Smiths.
--   The billing statement should take into account the Example Scenarios described on GP1.
--   After the bill is displayed on the screen, the user clicks a "check out" button.


CREATE OR REPLACE FUNCTION get_billing_statement(
    guest_first_name_param text,
    guest_last_name_param text,
    checkout_date_param TIMESTAMP)
RETURNS TABLE (
    guest_first_name VARCHAR(255),
    guest_last_name VARCHAR(255),
    reservation_id INT,
    checkin_date TIMESTAMP,
    checkout_date TIMESTAMP,
    days_stayed INT,
    room_num INT,
    room_price DECIMAL,
    total_discounted_price DECIMAL,
    total_service_price DECIMAL,
    total_amount_due DECIMAL
) AS $$
DECLARE
    current TIMESTAMP; -- current date
    guest_id_val INT;
    hotel_id_val INT;
    discount_for_day DECIMAL;
    total_discounted_price DECIMAL := 0; -- used to accumulate the total discounted price
    season_discount DECIMAL := 0;
    guest_category_discount DECIMAL := 0;
BEGIN
-- 	MAKE TOTALS
    total_service_price := 0;
    total_amount_due := 0;
    total_discounted_price := 0; -- initialized twice to make sure it is 0 (double sure lol)

-- GUEST ID
    SELECT guest_id INTO guest_id_val FROM guest WHERE first_name = guest_first_name_param AND last_name = guest_last_name_param;

-- HOTEL ID
    SELECT hotel_id INTO hotel_id_val FROM reservation WHERE guest_id = guest_id_val LIMIT 1;

-- CHECK IN AND CHECK OUT DATES
-- retrieves the earliest and latest check in and out dates
    SELECT MIN(r.checkin_date), MAX(r.checkout_date) INTO checkin_date, checkout_date FROM reservation r WHERE r.guest_id = guest_id_val;

-- DAYS STAYED
-- extract keyword used to get day from TIMESTAMP type
    days_stayed := EXTRACT(DAY FROM checkout_date - checkin_date);

-- SEASON FOR CURRENT DATE
-- make sure the discount is for the season
    SELECT COALESCE(discount, 0) INTO season_discount
    FROM seasons
    WHERE hotel_id = hotel_id_val
    AND checkout_date BETWEEN start_date AND end_date;


-- GUEST CATEGORY DISCOUNT
    SELECT COALESCE(discount, 0) INTO guest_category_discount
    FROM guest_category
    WHERE hotel_id = hotel_id_val
    AND guest_id = guest_id_val;

--     ITERATION FOR EACH DAY OF GUEST STAY
-- Necessary for calculating day discounts, but used for calculating general discounts also
-- https://www.postgresql.org/docs/current/functions-srf.html
    FOR current IN SELECT generate_series(checkin_date::date, checkout_date::date - 1, '1 day') LOOP
        -- price of room for current day
        SELECT rt.price INTO room_price
        FROM room_type rt
        JOIN reservation r ON rt.type_id = r.type_id AND rt.hotel_id = r.hotel_id
        WHERE r.checkin_date <= current AND r.checkout_date > current AND r.guest_id = guest_id_val;

--         DAY DISOCUNT
        discount_for_day := (SELECT COALESCE(discount, 0) FROM day_discount WHERE hotel_id = hotel_id_val AND weekday = EXTRACT(DOW FROM current));

--         APPLY ALL THE DISCOUNTS FOR THAT DAY
        total_discounted_price := total_discounted_price + (room_price * (1 - discount_for_day) * (1 - season_discount) * (1 - guest_category_discount));

    END LOOP;

-- GET ALL SERVICE PRICES
    SELECT COALESCE(SUM(price), 0) INTO total_service_price
    FROM (
        SELECT price FROM service WHERE guest_id = guest_id_val
        UNION ALL
        SELECT price FROM spa_service WHERE hotel_id = hotel_id_val AND service_id IS NOT NULL
    ) AS combo_services;


--     TOTAL AMOUNT CALCULATED
    total_amount_due := total_discounted_price + total_service_price;

-- RETURNS BILLING STATEMENT
    RETURN QUERY SELECT
        g.first_name,
        g.last_name,
        r.reservation_id,
        r.checkin_date,
        r.checkout_date,
        days_stayed,
        r.room_num,
        room_price,
        total_discounted_price,
        total_service_price,
        total_amount_due
    FROM
        reservation r
    JOIN
        guest g ON r.guest_id = g.guest_id
    WHERE
        r.guest_id = guest_id_val
        AND r.checkout_date = checkout_date_param
        AND r.actual_checkout IS NOT NULL;
END;
$$ LANGUAGE plpgsql STRICT;


-- CREATE OR REPLACE FUNCTION checkout_and_generate_bill(
--     guest_first_name_param TEXT,
--     guest_last_name_param TEXT,
--     checkout_time TIMESTAMP)
-- RETURNS VOID AS $$
-- DECLARE
--     guest_id_val INT;
--     total_due DECIMAL;
--     f_reservation_id INT;
--     f_checkout_date TIMESTAMP;
-- BEGIN
--     SELECT guest_id INTO guest_id_val FROM guest WHERE first_name = guest_first_name_param AND last_name = guest_last_name_param;
--     RAISE NOTICE 'Guest ID: %', guest_id_val;

--     -- update reservations with actual checkout date
--     SELECT reservation_id, actual_checkout INTO f_reservation_id, f_checkout_date FROM reservation WHERE guest_id = guest_id_val AND actual_checkout IS NULL LIMIT 1;
--     RAISE NOTICE 'Reservation ID: %, Checkout Date: %', f_reservation_id, f_checkout_date;
--     UPDATE reservation SET actual_checkout = checkout_time WHERE reservation_id = f_reservation_id;
--     RAISE NOTICE 'Checkout Time: %', checkout_time;

--     -- delete occupant from occupants
--     DELETE FROM occupant WHERE reservation_id = f_reservation_id;

--     -- update room status; set is_clean and is_occupied to False
--     UPDATE room SET is_clean = FALSE, is_occupied = FALSE WHERE room_num = (SELECT room_num FROM reservation WHERE reservation_id = f_reservation_id);

--     -- Get the total amount due from the billing statement
--     SELECT COALESCE(total_amount_due, 0) INTO total_due FROM get_billing_statement(guest_first_name_param, guest_last_name_param, checkout_time);
--     RAISE NOTICE 'Total Amount Due: %', total_due;

--     -- Need to update the bill

--     INSERT INTO bill (guest_id, bill_id, total, reservation_id) VALUES (guest_id_val, gen_random_uuid(), total_due, f_reservation_id);


--     -- mark the room as clean
--     UPDATE room SET is_clean = TRUE WHERE room_num IN (SELECT room_num FROM reservation WHERE reservation_id = f_reservation_id);
--     RAISE NOTICE 'New room clean status: %', (SELECT is_clean FROM room WHERE room_num IN (SELECT room_num FROM reservation WHERE reservation_id = f_reservation_id));

-- END;
-- $$ LANGUAGE plpgsql;
