WITH MAX_Duration_Mins as (
  SELECT F.origin, MAX(duration_mins) AS max_duration
  FROM Flights AS F
  GROUP BY F.origin
)
SELECT F.origin, F.fid, F.duration_mins
FROM Flights F
JOIN MAX_Duration_Mins AS M ON F.origin = M.origin AND F.duration_mins = M.max_duration;

