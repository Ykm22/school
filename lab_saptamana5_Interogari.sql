USE Ferma

SELECT *
FROM SpatiiDeAnimale

INSERT INTO SpatiiDeAnimale (nr_spatiu, nrMaximAnimale_spatiu, tip_spatiu)
VALUES (23, 10, 'oi')
INSERT INTO SpatiiDeAnimale (nr_spatiu, nrMaximAnimale_spatiu, tip_spatiu)
VALUES (45, 13, 'vaci')
INSERT INTO SpatiiDeAnimale (nr_spatiu, nrMaximAnimale_spatiu, tip_spatiu)
VALUES (25, 3, 'cai')
INSERT INTO SpatiiDeAnimale (nr_spatiu, nrMaximAnimale_spatiu, tip_spatiu)
VALUES (15, 20, 'rate')
INSERT INTO SpatiiDeAnimale (nr_spatiu, nrMaximAnimale_spatiu, tip_spatiu)
VALUES (30, 7, 'iepuri')
--ALTER TABLE SpatiiDeAnimale
--DROP COLUMN nr_spatiu
--DELETE FROM SpatiiDeAnimale
--WHERE cod_spatiu = 3

SELECT *
FROM Ingrijitori

SELECT *
FROM SpatiiDeAnimale

INSERT INTO Ingrijitori (nume_i, salariu_i, ore_i, cod_spatiu)
VALUES ('Emilian Emil', 555, 20, 1) 
INSERT INTO Ingrijitori (nume_i, salariu_i, ore_i, cod_spatiu)
VALUES ('Fabian Farner', 490, 25, 6) 
INSERT INTO Ingrijitori (nume_i, salariu_i, ore_i, cod_spatiu)
VALUES ('Marcel Maroc', 600, 34, 5) 

SELECT *
FROM Animale

--DELETE FROM Animale
--WHERE cod_a = 4 

INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Gaina', 'Minorca', 1)
INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Gaina', 'Friesian', 1)
INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Gaina', 'Sumatra', 1)
INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Gaina', 'Kulang', 1)

SELECT *
FROM Animale

ALTER TABLE Animale
DROP COLUMN greutate

UPDATE Animale
SET greutate_a = 10
WHERE descriere_a = 'Kulang'


INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Vaca', 'Angus', 4)
INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Vaca', 'Jersey', 4)
INSERT INTO Animale (specie_a, descriere_a, cod_spatiu)
VALUES ('Vaca', 'Malvi', 4)

UPDATE Animale
SET greutate_a = 700
WHERE descriere_a = 'Angus'

UPDATE Animale
SET greutate_a = 713
WHERE descriere_a = 'Jersey'

UPDATE Animale
SET greutate_a = 720
WHERE descriere_a = 'Malvi'

SELECT *
FROM SpatiiDeAnimale

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Cu cap castaniu', 6, 1)

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Cu ciuf', 6, 2)

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Pestrita', 6, 2)

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Pestrita', 6, 1)

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Pestrita', 6, 2)

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES ('Rata', 'Sulitar', 6, 1)

SELECT * 
FROM Furaje

INSERT INTO Furaje (nume_f, cantitate_f)
VALUES ('Intensive de ferma', 100)
INSERT INTO Furaje (nume_f, cantitate_f)
VALUES ('Semi-intensive', 80)
INSERT INTO Furaje (nume_f, cantitate_f)
VALUES ('Gospodaresti', 90)
INSERT INTO Furaje (nume_f, cantitate_f)
VALUES ('Inferioare', 95)

SELECT *
FROM Furaje
SELECT * 
from Animale
SELECT *
FROM AnimaleFuraje
ALTER TABLE AnimaleFuraje
ADD cantitate_af INT

INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (5, 1, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (6, 2, 30)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (6, 1, 10)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (7, 3, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (8, 3, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (9, 3, 10)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (10, 4, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (11, 4, 6)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (12, 4, 8)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (13, 4, 3)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (13, 1, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (14, 4, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (15, 2, 20)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (16, 4, 5)
INSERT INTO AnimaleFuraje(cod_a, cod_f, cantitate_af)
VALUES (17, 1, 5)

INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de gaina', 5)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de gaina', 6)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de gaina', 7)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('carne de gaina', 5)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('carnede gaina', 8)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('lapte de vaca', 9)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('lapte de vaca', 10)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('piele de vaca', 10)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('lapte de vaca', 11)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('piele de vaca', 11)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de rata', 12)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('pene de rata', 12)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de rata', 12)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('carne de rata', 13)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de rata', 14)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('pene de rata', 14)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de rata', 15)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('carne de rata', 16)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('oua de rata', 16)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('carne de rata', 16)
INSERT INTO MateriiPrime (nume_mp, cod_a)
VALUES ('pene de rata', 16)

SELECT * 
FROM MateriiPrime

INSERT INTO StatiiDeProcesare (tip_s) 
VALUES ('Care proceseaza oua')
INSERT INTO StatiiDeProcesare (tip_s) 
VALUES ('Care proceseaza carne')
INSERT INTO StatiiDeProcesare (tip_s) 
VALUES ('Care proceseaza pene')
INSERT INTO StatiiDeProcesare (tip_s) 
VALUES ('Care proceseaza lapte')
INSERT INTO StatiiDeProcesare (tip_s) 
VALUES ('Care proceseaza piele')

SELECT *
FROM StatiiDeProcesare
SELECT * 
FROM MateriiPrime
SELECT * 
FROM StatiiMaterii

--UPDATE MateriiPrime
--SET nume_mp = 'carne de gaina'
--WHERE nume_mp = 'carnede gaina'

INSERT INTO StatiiMaterii (cod_s, cod_mp)
VALUES (1, 1), (1, 2), (1, 3), (1, 13), (1, 11), (1, 15), (1, 17), (1, 19)
INSERT INTO StatiiMaterii (cod_s, cod_mp)
VALUES(2, 4), (2, 5), (2, 14), (2, 18), (2, 20)
INSERT INTO StatiiMaterii (cod_s, cod_mp)
VALUES (3, 12), (3, 16), (3, 21)
INSERT INTO StatiiMaterii (cod_s, cod_mp)
VALUES (4, 6), (4, 7), (4, 9)
INSERT INTO StatiiMaterii (cod_s, cod_mp)
VALUES (5, 8), (5, 10)

SELECT * 
FROM Ingrijitori
SELECT *
FROM Furaje
SELECT *
FROM ProduseFinite

INSERT INTO Magazin (nume_mag, castig_mag)
VALUES ('Magazinul1', 2000)
INSERT INTO Magazin (nume_mag, castig_mag)
VALUES ('Magazinul2', 1500)
INSERT INTO Magazin (nume_mag, castig_mag)
VALUES ('Magazinul3', 2500)

SELECT *
FROM Magazin
SELECT *
FROM StatiiDeProcesare

SELECT * 
FROM Muncitori

INSERT INTO Muncitori (nume_m, salariu_m, ore_m, cod_s)
VALUES ('Adriana Enache', 500, 25, 1), ('Adrian Codrea', 750, 30, 2), ('Marcel Menea', 600, 15, 3),('Marian Monol', 400, 15, 5)

SELECT * FROM StatiiDeProcesare
SELECT * FROM Animale
SELECT * FROM ProduseFinite

INSERT INTO ProduseFinite(nume_pf, cod_mag)
VALUES('oua lichide', 1), ('praf de oua', 1), ('oua lichide', 2), ('praf de oua', 3)
,('antricot de vita', 1), ('pula de vita', 1), ('coada de vita', 2), ('pastrama de vita', 3), ('carnati afumati de vita', 3),
('piept de pui', 1), ('pulpe de pui', 1), ('gheare de pui', 2), ('snitele de pui', 3)
,('iaurt', 2), ('branza de vaci', 2), ('cascaval de vaca', 2), ('unt', 3), ('telemea', 3)

SELECT * FROM StatiiProduse
SELECT * FROM ProduseFinite

INSERT INTO StatiiProduse(cod_s, cod_pf)
VALUES (1, 1), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2,7), (2,8), (2,9), (2,10),
(2, 11), (2,12), (2,13), (4,14), (4,15), (4,16), (4,17), (4,18)

SELECT * FROM Muncitori

SELECT * FROM SpatiiDeAnimale
SELECT * FROM Animale
SELECT  specie_a, greutate_a, cnt=COUNT(specie_a)
FROM Animale
GROUP BY specie_a, greutate_a
HAVING specie_a = 'Rata'

--Cate specii de animale sunt inregistrare in ferma?
SELECT A.specie_a, numar=COUNT(A.specie_a)
FROM Animale A
INNER JOIN SpatiiDeAnimale Spatii ON A.cod_spatiu = Spatii.cod_spatiu
GROUP BY A.specie_a

SELECT * 
FROM Animale
WHERE specie_a = 'Gaina'

--Cate subspecii de gaina sunt inregistrate in ferma
--care au media greutatilor mai mare ca 10 si nr de animale din acea subspecie?

SELECT A.descriere_a, numar=COUNT(A.descriere_a), greutate_avg=AVG(A.greutate_a)
FROM Animale A
INNER JOIN SpatiiDeAnimale Spatii ON A.cod_spatiu = Spatii.cod_spatiu
INNER JOIN AnimaleFuraje animFuraje ON animFuraje.cod_a = A.cod_a
WHERE A.specie_a = 'Gaina'
GROUP BY A.descriere_a
HAVING AVG(A.greutate_a) > 10

INSERT INTO Animale(specie_a, descriere_a, cod_spatiu, greutate_a)
VALUES('Gaina', 'Minorca', 1, 12), ('Gaina', 'Minorca', 1, 12)
--------------------------------------------------------------------------------------
------------------------------------LAB2----------------------------------------------
--------------------------------------------------------------------------------------
-------------
--1
-------------
--Animalele existente de la care s-a obtinut materie prima si spatiul lor?
--WHERE + >2 TABELE
SELECT A.cod_a, A.specie_a, A.descriere_a, Spatii.cod_spatiu, materiePrima.nume_mp
FROM Animale A, SpatiiDeAnimale Spatii, MateriiPrime materiePrima
WHERE A.cod_spatiu = Spatii.cod_spatiu AND A.cod_a = materiePrima.cod_a
ORDER BY nume_mp

SELECT * FROM Animale
SELECT * FROM MateriiPrime
SELECT * FROM SpatiiDeAnimale

-------------
--2
-------------
--Speciile de animale  m.a(greutate) > 10, care mananca furaje intensive de ferma 
--WHERE + GROUP BY + HAVING + M-N + >2 TABELE
SELECT A.specie_a, A.descriere_a, numar=COUNT(A.descriere_a)
FROM Animale A
INNER JOIN SpatiiDeAnimale spatii ON spatii.cod_spatiu = A.cod_spatiu
INNER JOIN AnimaleFuraje AF ON AF.cod_a = A.cod_a
INNER JOIN Furaje F ON F.cod_f = AF.cod_f
WHERE F.nume_f = 'Intensive de ferma'
GROUP BY A.specie_a, A.descriere_a
HAVING AVG(A.greutate_a) > 10

------------
--3
------------
--Care sunt speciile de animale care au facut oua
--WHERE + DISTINCT + >2TABELE
SELECT A.cod_a, A.specie_a, A.descriere_a, materiiPrime.cod_mp
FROM Animale A
INNER JOIN SpatiiDeAnimale Spatii ON A.cod_spatiu = Spatii.cod_spatiu
INNER JOIN MateriiPrime materiiPrime ON materiiPrime.cod_a = A.cod_a
WHERE materiiPrime.nume_mp = 'oua'


---------------
--4
---------------
--Care sunt statiile de procesare care au produse la magazin
--WHERE + DISTINCT + >2 TABELE + M-N
SELECT DISTINCT statii.tip_s
FROM StatiiDeProcesare statii
INNER JOIN StatiiProduse statiiProduse ON statiiProduse.cod_s = statii.cod_s
INNER JOIN ProduseFinite pf ON statiiProduse.cod_pf = pf.cod_pf
INNER JOIN Magazin mag ON mag.cod_mag = pf.cod_mag

SELECT * FROM Furaje
SELECT * FROM Animale
SELECT * FROM AnimaleFuraje

---------------------
--5
--------------------
--Cate specii de animale care mananca furaje gospodaresti
--WHERE + GROUP BY + >2 TABELE
SELECT A.specie_a, numar=COUNT(A.specie_a), spatii.cod_spatiu, AF.cantitate_af
FROM Animale A
INNER JOIN SpatiiDeAnimale spatii ON spatii.cod_spatiu = A.cod_spatiu
INNER JOIN AnimaleFuraje AF ON AF.cod_a = A.cod_a
INNER JOIN Furaje F ON F.cod_f = AF.cod_f
WHERE F.nume_f = 'Gospodaresti'
GROUP BY A.specie_a, spatii.cod_spatiu, F.nume_f, AF.cantitate_af

SELECT * FROM Animale
SELECT * FROM AnimaleFuraje

------------------------------
--6
----------------------------
--Subspeciile de gaina care au materii prime cu m.a.(greutatilor) > 10
--WHERE + GROUP BY + HAVING + >2 TABELE
SELECT A.descriere_a, numar=COUNT(A.descriere_a), greutate_avg=AVG(A.greutate_a), S.cod_spatiu
FROM Animale A
INNER JOIN SpatiiDeAnimale S ON S.cod_spatiu = A.cod_spatiu
INNER JOIN MateriiPrime MP ON A.cod_a = MP.cod_a
WHERE A.specie_a = 'Gaina'
GROUP BY A.descriere_a, S.cod_spatiu
HAVING AVG(A.greutate_a) > 10


----------------------
--7
----------------------
--Care sunt muncitorii unei care lucreaza la o statie ce a facut produs finit
--WHERE + DISTINCT + >2 TABELE
SELECT DISTINCT M.nume_m
FROM Muncitori M, StatiiDeProcesare S, StatiiProduse SP, ProduseFinite PF
WHERE M.cod_s = S.cod_s AND SP.cod_s = S.cod_s AND SP.cod_pf = PF.cod_pf

/*SELECT DISTINCT M.nume_m
FROM Muncitori M
INNER JOIN StatiiDeProcesare S ON S.cod_s = M.cod_s 
INNER JOIN StatiiProduse SP ON SP.cod_s = S.cod_s
INNER JOIN ProduseFinite PF ON PF.cod_pf = SP.cod_pf*/

SELECT * FROM MUNCITORI
SELECT * FROM StatiiDeProcesare
SELECT * FROM StatiiProduse
SELECT * FROM ProduseFinite

-------------
--8
-------------
--Cate produse se proceseaza la fiecare statie
SELECT S.tip_s, numar_produse=COUNT(SP.cod_pf)
FROM StatiiDeProcesare S
INNER JOIN StatiiProduse SP ON SP.cod_s = S.cod_s
INNER JOIN ProduseFinite PF ON SP.cod_pf = PF.cod_pf
GROUP BY S.tip_s

SELECT * FROM StatiiDeProcesare
SELECT * FROM StatiiProduse

---------------
--9
--------------
--Cati ingrijitori au grija de un spatiu?
SELECT S.cod_spatiu, numar_ingrijitori=COUNT(I.cod_spatiu)
FROM SpatiiDeAnimale S
INNER JOIN Ingrijitori I ON S.cod_spatiu = I.cod_spatiu
GROUP BY S.cod_spatiu

SELECT * FROM Ingrijitori

-----------------
--10
----------------
--Cate magazine au mai mult de 5 produse la vanzare
SELECT M.nume_mag, numar_produse=COUNT(PF.cod_mag)
FROM Magazin M
INNER JOIN ProduseFinite PF ON PF.cod_mag = M.cod_mag
GROUP BY M.nume_mag
HAVING COUNT(PF.cod_mag) > 5