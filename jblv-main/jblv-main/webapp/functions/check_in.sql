DROP FUNCTION IF EXISTS get_available_double_rooms(TIMESTAMP);

CREATE FUNCTION get_available_double_rooms(checkin TIMESTAMP)
RETURNS TABLE (
    reservation_id INT,
    guest_id INT
) AS $$
    SELECT res.guest_id, res.checkin_date, guest.first_name, guest.last_name
    FROM reservation res
    LEFT JOIN guest
	    ON res.guest_id = guest.guest_id
    WHERE res.checkin_date = checkin;

$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION get_available_double_rooms(checkin TIMESTAMP) OWNER TO jblv;
