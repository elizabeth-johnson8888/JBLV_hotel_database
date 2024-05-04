-- Query 4
--   Write a query for the special feature of your database that only your team has designed.
--   The query should be about as complex as the previous three.
--   After displaying the results of the query, the user should be able to click on
--   something that causes the database to be updated.
--   For example, your feature might involve streaming movies in hotel rooms.
--   The query would show available movies (title, rating, runtime, and other details) along with the rental cost.

DROP FUNCTION IF EXISTS get_spa_service(DECIMAL);

CREATE FUNCTION get_spa_service(max_price DECIMAL)
RETURNS TABLE (
    service_name VARCHAR(255),
    service_cat VARCHAR(255),
    price DECIMAL
) AS $$

  SELECT s.name, ss.name, ss.price
  FROM service s
  JOIN spa_service ss ON s.service_id = ss.service_id
  WHERE ss.price <= max_price
    AND ss.hotel_id = 0
  GROUP BY s.name, ss.name, ss.price
  ORDER BY ss.price DESC;

$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION get_spa_service(DECIMAL) OWNER TO jblv;