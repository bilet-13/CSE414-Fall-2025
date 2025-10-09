SELECT DISTINCT n.n_number, n.name, n.city
FROM N_Numbers AS n
JOIN Flights    AS f
  ON f.tail_num = n.n_number
WHERE f.cancelled = 0 AND 
  UPPER(TRIM(f.origin_city)) = UPPER(TRIM(n.city || ', ' || n.state)) AND
  n.year_mfr = '2024';
