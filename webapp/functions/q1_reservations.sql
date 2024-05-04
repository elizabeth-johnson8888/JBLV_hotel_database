-- Query 1: A registered guest would like to reserve a room in Hotel A from
-- July 15th (check-in) to July 17th (check-out). The guest is a "gold" customer.
-- The query should return all the different room types that are available in
--   the hotel for those two nights, along with be the average cost per night
--   for that room type (cost per night divided by # of nights).
--   The cost per night must take into account the current season and the days
--   of the week of the requested dates of stay, along with any special rates for "gold" customers.

DROP FUNCTION IF EXISTS q1_reservations(INT, DATE, DATE);

CREATE FUNCTION q1_reservations(hotel INT, checkin DATE, checkout DATE)
RETURNS TABLE (
    room_type VARCHAR(255),
    avg_cost_per_night FLOAT
) AS $$
  
  SELECT avg_sq.type_id, avg_price_per_night
  FROM (
      SELECT 
      available_rooms.type_id,
          AVG(night_price) AS avg_price_per_night
      FROM (
          SELECT 
          r.type_id,
              (rt.price * (gc.discount + s.discount + dd.discount)) AS night_price
      FROM room r
        LEFT JOIN reservation res ON r.hotel_id = res.hotel_id
          AND (res.checkin_date > DATE(checkout) OR res.checkout_date < DATE(checkin))
        JOIN room_type rt ON r.type_id = rt.type_id
          AND rt.hotel_id = r.hotel_id
        JOIN hotel h ON r.hotel_id = h.hotel_id
        JOIN guest_category gc ON gc.hotel_id = h.hotel_id
        JOIN seasons s ON s.hotel_id = h.hotel_id
        JOIN day_discount dd ON dd.hotel_id = h.hotel_id
          WHERE r.hotel_id = hotel
  -- 					returns 0-6, 0 = Sunday, 6 = Saturday
            AND dd.weekday BETWEEN EXTRACT(DOW FROM checkin::date) AND EXTRACT(DOW FROM checkout::date)
            AND s.season_name = 'Spring'
            AND gc.name = 'VIP'
    ) AS available_rooms
    GROUP BY type_id
  ) AS avg_sq
  GROUP BY avg_sq.type_id, avg_price_per_night
  ORDER BY avg_sq.type_id asc;
    
$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION q1_reservations(hotel INT, checkin DATE, checkout DATE) OWNER TO jblv;
