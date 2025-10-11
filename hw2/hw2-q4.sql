SELECT DISTINCT F1.tail_num AS tail_number,
  F1.origin   AS airport

FROM Flights AS F1
JOIN Flights AS F2 ON F1.tail_num = F2.tail_num AND 
  F1.year = F2.year AND 
  F1.month = F2.month AND 
  F1.day_of_month = F2.day_of_month AND 
  F1.origin = F2.origin AND 
  F1.dest <> F2.dest AND 
  F1.fid   <  F2.fid        

WHERE F1.cancelled = 0 AND 
  F2.cancelled = 0 AND 
  (F1.distance_mi + F2.distance_mi) >= 5200;
