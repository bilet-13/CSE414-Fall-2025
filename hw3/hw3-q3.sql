WITH flight_top20 AS(SELECT
  F.origin,
  F.origin_city,
  F.dest,
  F.dest_city,
  COUNT(*) AS num_flights
FROM Flights AS F
GROUP BY F.origin, F.origin_city, F.dest, F.dest_city
ORDER BY num_flights DESC
LIMIT 20),
flight_once AS(SELECT
  F.origin,
  F.origin_city,
  F.dest,
  F.dest_city,
  COUNT(*) AS num_flights
FROM Flights AS F
GROUP BY F.origin, F.origin_city, F.dest, F.dest_city
HAVING COUNT(*) = 1)
SELECT * FROM flight_top20
UNION
SELECT * FROM flight_once
ORDER BY num_flights, origin, dest;
