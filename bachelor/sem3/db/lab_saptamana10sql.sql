select * from magazin

insert into magazin (nume_mag, castig_mag)
values ('Magazinul4', 1250), ('Magazinul5', 1320), ('Magazinul6', 1700), ('Magazinul7', 2300)

select * from tables
select * from Magazin
select * from Animale

insert into tables (name) values ('Magazin'), ('Animale'), ('vw_Muncitori')

select * from TestTables
select * from tables

insert into TestTables (TestID, TableID, NoOfRows, Position)
values(1, 1, 4, 1), (1, 2, 10, 2), (1, 3, 3, 3) 

select * from TestRunTables
select * from TestTables
select * from TestRuns
select * from tests

ALTER PROCEDURE runTest @test_nr INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @time_start VARCHAR(100)
	SET @time_start = getdate()

	DECLARE @test_description VARCHAR(100)
	SET @test_description = 'Rularea testului ' + CONVERT(VARCHAR(100), @test_nr)

	INSERT INTO TestRuns (Description, StartAt)
	VALUES (@test_description, @time_start);

	DECLARE @testRunId INT;
	SELECT @testRunId = TestRunID FROM TestRuns WHERE Description = @test_description AND StartAt = @time_start;

	EXEC deleteTest @test_nr, @testRunId
	EXEC insertTest @test_nr, @testRunId
	EXEC viewsTest @test_nr, @testRunId

	UPDATE TestRuns 
	SET EndAt = GETDATE()
	WHERE TestRunID = @testRunId
END


exec runTest 1

select * from TestRuns
select * from TestRunTables
select * from TestRunViews

delete from TestRuns
delete from TestRunTables
delete from TestRunViews

select * from muncitori
select * from magazin
select * from animale

delete from muncitori
delete from magazin
delete from animale

ALTER PROCEDURE deleteTest @test_nr INT, @testRunId INT AS
BEGIN 
	SET NOCOUNT ON
	DECLARE cursorDeleteTest CURSOR FAST_FORWARD  FOR
	SELECT TableID, NoOfRows FROM getTestTables(@test_nr) ORDER BY Position;
	OPEN cursorDeleteTest;
	
	DECLARE @tableID INT, @NoOfRows INT;

	FETCH NEXT FROM cursorDeleteTest INTO @tableID, @NoOfRows;
	WHILE @@FETCH_STATUS = 0
	BEGIN
		--INSERT INTO TestRunTables (TestRunID, TableID, StartAt, EndAt)
		--VALUES (@testRunId, @tableID, GETDATE(), GETDATE())
		

		EXEC deleteEntries @tableID

		FETCH NEXT FROM cursorDeleteTest INTO @tableID, @NoOfRows;

	END
	CLOSE cursorDeleteTest;
	DEALLOCATE cursorDeleteTest;
END
	

ALTER PROCEDURE insertTest @test_nr INT, @testRunId INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE cursorInsertTest CURSOR FAST_FORWARD FOR
	SELECT TableID, NoOfRows FROM getTestTables(@test_nr) ORDER BY Position DESC;
	OPEN cursorInsertTest;

	DECLARE @tableID INT, @NoOfRows INT;
	FETCH NEXT FROM cursorInsertTest INTO @tableID, @NoOfRows;
	DECLARE @my_start DATETIME;
	
	WHILE @@FETCH_STATUS = 0
	BEGIN

		SET @my_start = SYSDATETIME()

		EXEC insertEntries @tableID, @NoOfRows
		

		INSERT INTO TestRunTables (TestRunID, TableID, StartAt, EndAt)
		VALUES (@testRunId, @tableID, @my_start, GETDATE())

		FETCH NEXT FROM cursorInsertTest INTO @tableID, @NoOfRows;
		--update TestRunTables
		--set StartAt = @start
		--where TestRunID = @testRunId
		
		--update TestRunTables
		--set EndAt = GETDATE()
		--where TestRunID = @testRunId
	END
	CLOSE cursorInsertTest;
	DEALLOCATE cursorInsertTest;
END

ALTER PROCEDURE viewsTest @test_nr INT, @testRunId INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE cursorViewsTest CURSOR FAST_FORWARD FOR
	SELECT ViewID FROM getTestViews(@test_nr);
	OPEN cursorViewsTest


	DECLARE @view_ID INT;
	FETCH NEXT FROM cursorViewsTest INTO @view_ID
	DECLARE @start_view_time DATETIME;
	WHILE @@FETCH_STATUS = 0
	BEGIN
		SET @start_view_time = SYSDATETIME()

		EXEC callView @view_ID

		INSERT INTO TestRunViews (TestRunID, ViewID, StartAt, EndAt)
		VALUES (@testRunId, @view_ID, @start_view_time, GETDATE())

		FETCH NEXT FROM cursorViewsTest INTO @view_ID
	END

	CLOSE cursorViewsTest
	DEALLOCATE cursorViewsTest
END

CREATE PROCEDURE callView @view_ID INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @view_name VARCHAR(100)
	SELECT @view_name = name FROM Views
	WHERE ViewID = @view_ID

	IF @view_name = 'view_Furaje'
		SELECT * FROM view_Furaje
	IF @view_name = 'view_IngrijitoriActivi'
		SELECT * FROM view_IngrijitoriActivi
	IF @view_name = 'view_IngrijitoriActiviPerSalariu'
		SELECT * FROM view_IngrijitoriActiviPerSalariu
END

select * from magazin
delete from magazin

exec runTest 1
select * from TestRuns
select * from TestRunTables
select * from TestRunViews


ALTER PROCEDURE insertEntries @tableID INT, @NoOfRows INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @table_name VARCHAR(30)
	SELECT @table_name = name FROM Tables WHERE TableID = @tableID

	IF @table_name = 'Magazin'
		EXEC insertMagazin @NoOfRows
	IF @table_name = 'Animale'
		EXEC insertAnimale @NoOfRows
	IF @table_name = 'Muncitori'
		EXEC insertMuncitori @NoOfRows
END

CREATE PROCEDURE insertMuncitori @NoOfRows INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @cnp_m VARCHAR(30), @nume_m INT, @salariu_m INT, @ore_m INT;
	WHILE @NoOfRows > 0
	BEGIN
		SET @cnp_m = CONVERT(varchar(100), @NoOfRows);
		INSERT INTO Muncitori (cnp_m, nume_m, salariu_m, ore_m)
		VALUES (@cnp_m, @NoOfRows, @NoOfRows, @NoOfRows)
		SET @NoOfRows = @NoOfRows - 1
	END
END

ALTER PROCEDURE insertMagazin @NoOfRows INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @nume_mag VARCHAR(30), @castig_mag INT;
	WHILE @NoOfRows > 0
	BEGIN
		SET @nume_mag = CONVERT(varchar(100), @NoOfRows);
		INSERT INTO Magazin (nume_mag, castig_mag)
		VALUES (@nume_mag, @NoOfRows)
		SET @NoOfRows = @NoOfRows - 1
	END
END

CREATE PROCEDURE insertAnimale @NoOfRows INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @specie_a VARCHAR(30), @descriere_a VARCHAR(30), @greutate INT
	WHILE @NoOfRows > 0
	BEGIN
		SET @specie_a = CONVERT(varchar(100), @NoOfRows);
		SET @descriere_a = CONVERT(varchar(100), @NoOfRows);
		INSERT INTO Animale (specie_a, descriere_a, greutate_a)
		VALUES (@specie_a, @descriere_a, @NoOfRows);
		SET @NoOfRows = @NoOfRows - 1
	END
END

ALTER PROCEDURE deleteEntries @tableID INT AS
BEGIN
	SET NOCOUNT ON
	DECLARE @table_name VARCHAR(30)
	SELECT @table_name = name FROM Tables WHERE TableID = @tableID

	IF @table_name = 'Magazin'
		DELETE FROM Magazin
	IF @table_name = 'Animale'
		DELETE FROM Animale
	IF @table_name = 'Muncitori'
		DELETE FROM Muncitori

END

CREATE FUNCTION getTable(@id INT)
RETURNS TABLE AS
	RETURN SELECT * FROM Tables WHERE TableID=@id 

CREATE FUNCTION getTestTables(@id INT) 
RETURNS TABLE AS
	RETURN SELECT * FROM TestTables WHERE TestID = @id

CREATE FUNCTION getTestViews(@id INT)
RETURNS TABLE AS
	RETURN SELECT * FROM TestViews WHERE TestID = @id

ALTER VIEW view_Furaje AS
SELECT * FROM Furaje

CREATE VIEW view_IngrijitoriActivi AS
SELECT I.nume_i FROM Ingrijitori I
INNER JOIN SpatiiDeAnimale Sp ON I.cod_spatiu = Sp.cod_spatiu

CREATE VIEW view_IngrijitoriActiviPerSalariu AS
SELECT ingrijitori_amount = COUNT(*), salariu = i.salariu_i FROM Ingrijitori i
INNER JOIN SpatiiDeAnimale Sp ON i.cod_spatiu = Sp.cod_spatiu
GROUP BY salariu_i

select * from testtables
select * from tables

update testtables
set NoOfRows = 250
WHERE TableId = 4


drop table Muncitori
create table Muncitori(
	cod_m INT IDENTITY,
	cnp_m VARCHAR(100),
	nume_m VARCHAR(100),
	salariu_m INT,
	ore_m INT,
	cod_s INT,
	PRIMARY  KEY (cod_m, cnp_m),
	FOREIGN KEY (cod_s) REFERENCES StatiiDeProcesare(cod_s)
)
