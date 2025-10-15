WITH percentage AS (
  SELECT cid, 
    SUM(CASE WHEN cancelled = 0 THEN 1 ELSE 0 END) as non_cancelled_flights,    SUM(CASE WHEN cancelled = 0 AND arr_delay <= 0 THEN 1 ELSE 0 END) as on_time_flights
    FROM Flights 
    GROUP BY cid
)
SELECT C.cname as carrier_name, CASE WHEN COALESCE(P.non_cancelled_flights, 0) = 0 THEN 0.0 ELSE (P.on_time_flights * 100.0) / P.non_cancelled_flights END as on_time_pct
FROM Carriers as C
LEFT JOIN percentage as P ON C.cid = P.cid
ORDER BY on_time_pct DESC, C.cname;
