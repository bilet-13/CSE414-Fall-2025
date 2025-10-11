SELECT DISTINCT F.year, F.month, F.day_of_month, C.cname, F.op_carrier_flight_num as flight_num
FROM Flights AS F
JOIN Carriers AS C
  ON F.cid = C.cid
JOIN N_Numbers AS N
  ON F.tail_num = N.n_number
JOIN Aircraft_Types AS A
  ON N.mfr_mdl_code = A.atid
JOIN Cancellation_Codes AS CC
  ON F.cancellation_code = CC.ccid
WHERE f.cancelled = 1 AND 
  UPPER(TRIM(f.origin_city)) = UPPER("Atlanta, GA") AND
  A.model LIKE "%737%" AND LOWER(CC.description) LIKE "%weather%";
