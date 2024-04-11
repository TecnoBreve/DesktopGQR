SELECT
Es.QRCode,
Es.Descricao,
Es.Id,
(SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
FROM Estrutura ES
INNER JOIN dw_vista.dbo.DM_ESTRUTURA E
ON E.Id_Estrutura = Es.Id
WHERE E.CRno = 42636
AND Es.Tipo LIKE '%%'
AND Es.Nivel >= 3