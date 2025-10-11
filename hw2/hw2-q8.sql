SELECT C.description AS cancellation_reason, COUNT(F.cancellation_code) AS num_flights
FROM Cancellation_Codes AS C
LEFT JOIN Flights AS F
  ON F.cancellation_code = C.ccid
GROUP BY C.description;

