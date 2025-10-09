SELECT
  F.tail_num AS tail_num,
  C.cname AS carrier,
  AT.mfr AS mfr,
  AT.model AS model,
  COUNT(*) AS cnt

FROM Flights AS F
JOIN Carriers AS C  ON F.cid = C.cid
JOIN N_Numbers AS N  ON F.tail_num = N.n_number
JOIN Aircraft_Types AS AT ON N.mfr_mdl_code = AT.atid

WHERE F.cancelled = 0 

GROUP BY N.n_number
ORDER BY cnt DESC, tail_num ASC
LIMIT 25;
