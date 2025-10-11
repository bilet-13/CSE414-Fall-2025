SELECT
  C.cname AS carrier_name,
  F1.op_carrier_flight_num AS f1_flight_num,
  F1.duration_mins AS f1_duration_mins,
  F1.dest_city AS intermediate_city,
  F2.op_carrier_flight_num AS f2_flight_num,
  F2.duration_mins AS f2_duration_mins,
  (F1.duration_mins + F2.duration_mins)  AS total_duration_mins

FROM Flights AS F1
JOIN Flights AS F2 ON 
    F1.cid = F2.cid AND 
    F1.year = F2.year AND 
    F1.month = F2.month AND 
    F1.day_of_month = F2.day_of_month AND 
    F1.dest = F2.origin  
JOIN Carriers AS C ON 
    C.cid = F1.cid

WHERE
  F1.cancelled = 0 AND 
  F2.cancelled = 0 AND 
  F1.year = 2024 AND 
  F1.month = 9 AND 
  F1.day_of_month = 7 AND 
  F1.origin = 'SEA' AND 
  F2.dest_city = 'Chicago, IL' AND 
  F1.dep_time < F2.dep_time AND 
  (F1.duration_mins + F2.duration_mins) < 360

ORDER BY total_duration_mins, carrier_name, f1_flight_num, f2_flight_num;
