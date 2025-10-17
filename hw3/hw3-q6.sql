WITH Connection_Factor as(
  SELECT 
    F.origin,
    COUNT(DISTINCT F.dest) as connection_factor
  FROM Flights AS F
  GROUP BY F.origin
), Origin_Dest_Factor as(
SELECT
F.origin,
CF1.connection_factor AS origin_factor,
F.dest,
CF2.connection_factor AS dest_factor
FROM Flights AS F
JOIN Connection_Factor AS CF1 ON F.origin = CF1.origin
JOIN Connection_Factor AS CF2 ON F.dest = CF2.origin
), Strictly_Increasing_Factor_Origin AS(
  SELECT O.origin
  FROM Origin_Dest_Factor AS O
  GROUP BY O.origin
  HAVING O.origin_factor < MIN(O.dest_factor)
)
SELECT DISTINCT F.origin AS airport
FROM Flights as F
JOIN Strictly_Increasing_Factor_Origin AS SIO ON F.origin = SIO.origin
ORDER BY F.origin;
