WITH top10 AS (
    SELECT DISTINCT distance_mi
    FROM Flights 
    ORDER BY distance_mi DESC
    LIMIT 10
)
SELECT C.cname as carrier_name, F.origin, F.dest, F.distance_mi, COUNT(*) as num_flights
FROM Flights as F
JOIN Carriers as C ON F.cid = C.cid
WHERE F.distance_mi IN (SELECT distance_mi FROM top10)
GROUP BY C.cname, F.origin, F.dest, F.distance_mi
ORDER BY F.distance_mi DESC, F.origin, F.dest, C.cname;
