DROP FUNCTION IF EXISTS get_available_double_rooms(DATE, INT);

CREATE FUNCTION get_available_double_rooms(checkin DATE, hotelid INT)
RETURNS TABLE (
    room_num INT,
    floor_num INT
) AS $$
    SELECT room.room_num, room.floor_num
    FROM room
    LEFT JOIN reservation res
        ON room.room_num = res.room_num
        AND checkin BETWEEN res.checkin_date AND res.checkout_date
        AND res.hotel_id = hotelid
    WHERE room.type_id = 'Double Suite'
        AND room.is_clean = TRUE
        AND room.is_occupied = FALSE
        AND res.room_num IS NULL;

$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION get_available_double_rooms(checkin DATE, hotelid INT) OWNER TO jblv;
