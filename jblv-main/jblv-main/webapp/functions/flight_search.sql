--
-- List all flights departing from an airport between start and end dates.
--

DROP FUNCTION IF EXISTS flight_search(airport text, beg_date date, end_date date);

CREATE FUNCTION flight_search(airport text, beg_date date, end_date date)
RETURNS SETOF flight AS $$

  SELECT *
  FROM flight
  WHERE departure_airport = $1
    AND scheduled_departure > $2
    AND scheduled_departure < $3

$$ LANGUAGE SQL STABLE STRICT;

ALTER FUNCTION flight_search(airport text, beg_date date, end_date date) OWNER TO absent;
