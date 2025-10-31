CREATE TABLE Sales (
  name VARCHAR(40),
  discount VARCHAR(40),
  month VARCHAR(20),
  price INT
);


SELECT name
FROM Sales
GROUP BY name
HAVING COUNT(DISTINCT price) > 1;
-- The result is 0 rows. It means that the name -> price is a functional dependency.

SELECT month
FROM Sales
GROUP BY month
HAVING COUNT(DISTINCT discount) > 1;
-- The result is 0 rows. It means that the month -> discount is a functional dependency.

SELECT name
FROM Sales
GROUP BY name
HAVING COUNT(DISTINCT discount) > 1;
-- The result is not 0 rows. It means that the name -> discount is NOT a functional dependency.

CREATE TABLE Prices (
  name VARCHAR(40) PRIMARY KEY,
  price INT
);

CREATE TABLE Disounts (
  month VARCHAR(20) PRIMARY KEY,
  discount VARCHAR(40) 
);

CREATE TABLE Months (
  month VARCHAR(20),
  name VARCHAR(40),
  FOREIGN KEY (month) REFERENCES Disounts(month),
  FOREIGN KEY (name) REFERENCES Prices(name)
);

INSERT INTO Prices (name, price)
SELECT DISTINCT name, price
FROM Sales;
-- The size of Prices is 36 rows after the insertion.

INSERT INTO Disounts (month, discount)
SELECT DISTINCT month, discount
FROM Sales;
-- The size of Disounts is 12 rows after the insertion.

INSERT INTO Months (month, name)
SELECT DISTINCT month, name
FROM Sales;
-- The size of Months is 426 rows after the insertion.





