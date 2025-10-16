WITH Flights_Per_Day as(
  SELECT
    F.cid,
    F.year,
    F.month,
    F.day_of_month,
    SUM(CASE WHEN F.cancelled = 0 AND F.arr_delay <= 15.0 THEN 1 ELSE 0 END) as flights_timely,
    COUNT(*) as flight_total
  FROM Flights AS F
  GROUP BY F.cid, F.year, F.month, F.day_of_month
), Timely_Percentenage as(
  SELECT
    per_day.cid,
    per_day.year,
    per_day.month,
    per_day.day_of_month,
    (per_day.flights_timely * 100.0) / per_day.flight_total as pct_timely
    FROM Flights_Per_Day AS per_day
), Carriers_Timely as(
  SELECT
    T.cid
  FROM Timely_Percentenage AS T
  GROUP BY T.cid
  HAVING MIN(T.pct_timely) >= 70.0
)
SELECT DISTINCT C.cname as carrier_name
FROM Carriers as C, Carriers_Timely as CT
WHERE C.cid = CT.cid
ORDER BY C.cname;


