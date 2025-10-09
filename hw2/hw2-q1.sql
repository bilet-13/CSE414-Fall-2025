SELECT DISTINCT C.cname
FROM Flights F, Carriers C
WHERE F.cid == C.cid AND
      F.origin = 'SEA' AND 
      F.dest_city = 'Chicago, IL';
