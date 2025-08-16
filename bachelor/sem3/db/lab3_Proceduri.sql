USE FERMA
------------------------------------
--V0 -> V1
------------------------------------
ALTER PROCEDURE createVanzatoriTable AS
BEGIN
	CREATE TABLE Vanzatori(
	cod_v INT PRIMARY  KEY IDENTITY,
	nume_v VARCHAR(100),
	salariu_v INT,
	cod_mag INT);
END
GO

----------------------------------
--V1 -> V0
----------------------------------
CREATE PROCEDURE dropVanzatoriTable AS
BEGIN
	DROP TABLE Vanzatori;
END

----------------------------------
--V1 -> V2
----------------------------------
ALTER PROCEDURE addColumnVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	ADD ore_v INT;
END
GO

----------------------------------
--V2 -> V1
----------------------------------
ALTER PROCEDURE dropColumnVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	DROP COLUMN ore_v
END
GO

----------------------------------
--V2 -> V3
----------------------------------
CREATE PROCEDURE modifyNumeVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	ALTER COLUMN nume_v	 NVARCHAR(100) NULL;
END
GO

----------------------------------
--V3 -> V2
----------------------------------
CREATE PROCEDURE undoModifyNumeVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	ALTER COLUMN nume_v VARCHAR(100) NULL;
END
GO

----------------------------------
--V3 ->V4
----------------------------------
CREATE PROCEDURE addDefaultConstraintSalariuVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	ADD CONSTRAINT default_constraint
	DEFAULT 1500 FOR salariu_v;
END
GO

----------------------------------
--V4 -> V3
----------------------------------
CREATE PROCEDURE dropDefaultConstraintSalariuVanzatori AS
BEGIN
	ALTER TABLE Vanzatori
	DROP CONSTRAINT default_constraint;
END
GO

----------------------------------
--V4 -> V5
----------------------------------
ALTER PROCEDURE addFKConstraintVanzatoriToMagazin AS
BEGIN
	ALTER TABLE Vanzatori
	ADD CONSTRAINT FK_VanzatoriMagazin
	FOREIGN KEY (cod_mag) REFERENCES Magazin(cod_mag);
END
GO

----------------------------------
-- V5 -> V4
----------------------------------
CREATE PROCEDURE dropFKConstraintVanzatoriToMagazin AS
BEGIN
	ALTER TABLE Vanzatori
	DROP CONSTRAINT FK_VanzatoriMagazin;
END
GO

SELECT * FROM Vanzatori
EXEC createVanzatoriTable
EXEC dropVanzatoriTable
EXEC addColumnVanzatori
EXEC dropColumnVanzatori
EXEC modifyNumeVanzatori
EXEC undoModifyNumeVanzatori
EXEC addCHKConstraintSalariuVanzatori
EXEC dropCHKConstraintSalariuVanzatori
EXEC addFKConstraintVanzatoriToMagazin
EXEC dropFKConstraintVanzatoriToMagazin

CREATE TABLE CurrentTableVersion (current_version INT);
INSERT INTO CurrentTableVersion (current_version) VALUES (1)
SELECT * FROM CurrentTableVersion

----------------------------------
--update procedure
----------------------------------
ALTER PROCEDURE UpdateVanzatori @update_version INT AS
BEGIN
	--input between 0 and 5
	IF(@update_version < 0 OR @update_version > 5)
		RAISERROR('Give a table version between 0 and 5', 11, 1);
	ELSE
	BEGIN
		--obtaining current version from the table
		DECLARE @current_version INT
		SELECT @current_version = current_version
		FROM CurrentTableVersion current_version

		--making do's or undo's according to update_version requested
		IF(@current_version = @update_version)
			RAISERROR('Already at this version', 11, 1);
		IF(@current_version < @update_version)
			EXEC doChanges @current_version, @update_version;
		IF(@current_version > @update_version)
			EXEC undoChanges @current_version, @update_version;
	
		--updating current version in our table
	
		UPDATE CurrentTableVersion
		SET current_version = @update_version;
	END
END
GO

--do procedure	
ALTER PROCEDURE doChanges @current_version INT, @update_version INT AS
BEGIN
	--while loop which calls certain procedures until current version reaches 
	--requested version
	WHILE(@current_version < @update_version)
	BEGIN
		IF(@current_version = 0)
			EXEC createVanzatoriTable;
		IF(@current_version = 1)
			EXEC addColumnVanzatori
		IF(@current_version = 2)
			EXEC modifyNumeVanzatori
		IF(@current_version = 3)
			EXEC addDefaultConstraintSalariuVanzatori
		IF(@current_version = 4)
			EXEC addFKConstraintVanzatoriToMagazin
		SET @current_version = @current_version + 1
	END
END
GO

--undo procedure
ALTER PROCEDURE undoChanges @current_version INT, @update_version INT AS
BEGIN
	--while loop which calls certain procedures until current version reaches 
	--requested version
	WHILE(@current_version > @update_version)
	BEGIN
		IF(@current_version = 5)
			EXEC dropFKConstraintVanzatoriToMagazin;
		IF(@current_version = 4)
			EXEC dropDefaultConstraintSalariuVanzatori
		IF(@current_version = 3)
			EXEC undoModifyNumeVanzatori
		IF(@current_version = 2)
			EXEC dropColumnVanzatori
		IF(@current_version = 1)
			EXEC dropVanzatoriTable
		SET @current_version = @current_version - 1
	END
END
GO

select * from Vanzatori
select * from Magazin

UPDATE CurrentTableVersion
SET current_version = 0

EXEC UpdateVanzatori 10
select * from CurrentTableVersion

DROP TABLE Vanzatori

