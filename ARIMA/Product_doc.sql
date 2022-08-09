SELECT 
A.SalesOrderID,
A.OrderQty,
A.ProductID,
A.UnitPrice,
A.LineTotal,
B.DocumentNode
FROM Sales.SalesOrderDetail A
LEFT JOIN Production.ProductDocument B
ON A.ProductID=B.ProductID
ORDER BY B.DocumentNode DESC
