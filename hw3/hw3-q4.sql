WITH Competition_Factor as(
SELECT
  F.origin,
  F.dest,
  COUNT(DISTINCT F.cid) as factor
FROM Flights AS F
GROUP BY F.origin, F.dest)
SELECT factor, COUNT(*) as num_routes
FROM Competition_Factor
GROUP BY factor
ORDER BY factor DESC;

