use ferma

select * from animale

select * from materiiprime
select * from StatiiMaterii
select * from StatiiDeProcesare

exec addMateriePrima 'ceva', 21903

alter procedure addMateriePrima @nume_mp VARCHAR(100), @cod_a int AS
BEGIN
	set nocount on;
	if (dbo.validateMateriePrima(@nume_mp, @cod_a) = 0)
		throw 50003, 'Numele materiei prime este nule sau codul animalului inexistent', 1;
	else
		insert into MateriiPrime (nume_mp, cod_a)
		values (@nume_mp, @cod_a);
END

alter function validateMateriePrima (@nume_mp varchar(100), @cod_a int) returns bit as
begin
	if (not exists(select * from animale where cod_a = @cod_a))
		return 0;
	if (@nume_mp is null)
		return 0;
	return 1;
end

alter procedure readMateriiPrimeDupaAnimal @cod_a int as
begin
	set nocount on;
	select cod_mp, MateriePrima = nume_mp from MateriiPrime where cod_a = @cod_a
end

create procedure updateNumeMateriePrima @cod_mp int, @nume_nou varchar(100) as
begin
	set nocount on;
	update MateriiPrime
	set nume_mp = @nume_nou
	where cod_mp = @cod_mp;
end

create procedure deleteMateriePrima @cod_mp int as
begin
	set nocount on;
	delete from MateriiPrime
	where cod_mp = @cod_mp;
end

select * from MateriiPrime

exec readMateriiPrimeDupaAnimal 21904
exec deleteMateriePrima 39
exec addMateriePrima 'oua', 21904
exec updateNumeMateriePrima 40, 'pene'


create index IX_MateriiPrime_numeMP_asc on MateriiPrime (nume_mp ASC, cod_a ASC);
drop index IX_MateriiPrime_numeMP_asc ON MateriiPrime
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------

select * from StatiiDeProcesare

create procedure addStatieDeProcesare @tip_s varchar(100) as
begin
	set nocount on;
	if (dbo.validateStatieDeProcesare(@tip_s) = 0)
		throw 50004, 'Tipul statiei de procesare nu poate fi nul', 1;
	else
		insert into StatiiDeProcesare (tip_s) values (@tip_s)
end

create function validateStatieDeProcesare (@tip_s varchar(100)) returns bit as
begin
	if (@tip_s is null)
		return 0;
	return 1;
end

create procedure readStatiiDeProcesareDupaTip @tip_s varchar(100) as
begin	
	set nocount on;
	select * from StatiiDeProcesare where tip_s = @tip_s;
end

create procedure updateStatieDeProcesare @cod_s int, @tip_nou varchar(100) as
begin
	set nocount on;
	update StatiiDeProcesare
	set tip_s = @tip_nou
	where cod_s = @cod_s;
end

create procedure deleteStatieDeProcesare @cod_s int as
begin
	set nocount on;
	delete from StatiiDeProcesare where cod_s = @cod_s;
end

select * from StatiiDeProcesare
exec readStatiiDeProcesareDupaTip 'Care proceseaza carne'
exec deleteStatieDeProcesare 19
exec addStatieDeProcesare 'Care proceseaza carne'
exec updateStatieDeProcesare 20, 'Care proceseaza oua'


select * from StatiiDeProcesare
select * from StatiiMaterii
select * from MateriiPrime

---------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------

select * from StatiiMaterii

alter procedure addStatiiMaterii @cod_s int, @cod_mp int as
begin
	set nocount on;
	if (dbo.validateStatiiMaterii(@cod_s, @cod_mp) = 0)
		throw 50005, 'Statie sau materie prima invalida', 1;
	else
		insert into StatiiMaterii (cod_s, cod_mp) values (@cod_s, @cod_mp);
end
select * from StatiiDeProcesare order by tip_s
select * from StatiiMaterii
select * from MateriiPrime


create function validateStatiiMaterii (@cod_s int, @cod_mp int) returns bit as
begin
	if (not exists (select * from StatiiDeProcesare where cod_s = @cod_s))
		return 0;
	if (not exists (select * from MateriiPrime where cod_mp = @cod_mp))
		return 0;
	return 1;
end

create procedure readStatiiMaterii_byStatii @cod_s int as
begin
	select * from StatiiMaterii where cod_s = @cod_s;
end


create procedure updateStatiiMaterii_materie_byStatie @cod_s int, @cod_mp_vechi int, @cod_mp_nou int as
begin
	set nocount on;
	update StatiiMaterii
	set cod_mp = @cod_mp_nou
	where cod_s = @cod_s and cod_mp = @cod_mp_vechi;
end

create procedure deleteStatiiMaterii @cod_s int, @cod_mp int as
begin
	set nocount on;
	delete from StatiiMaterii
	where cod_s = @cod_s and cod_mp = @cod_mp;
end

select * from StatiiDeProcesare
select * from MateriiPrime
select * from StatiiMaterii
exec addStatiiMaterii 19, 100
exec readStatiiMaterii_byStatii 20
exec addStatiiMaterii 20, 27
exec updateStatiiMaterii_materie_byStatie 20, 27, 28  
exec deleteStatiiMaterii 20, 28

--create index IX_StatiiMaterii_codS_asc_codMP_asc ON StatiiMaterii (cod_s ASC, cod_mp ASC);

-----------------------------------------------------------------------------------------------------------------------------------
alter view vw_StatiiDeProcesare_deCarne as
	select cod_s from StatiiDeProcesare where tip_s = 'Care proceseaza carne'
select * from vw_StatiiDeProcesare_deCarne

create index ix_StatiiDeProcesare_tipS_asc ON StatiiDeProcesare(tip_s ASC)
--drop index ix_StatiiDeProcesare_tipS_asc ON StatiiDeProcesare

select * from StatiiDeProcesare

alter view vw_StatiiDeProcesare_Active as
	select distinct sm.cod_s, s.tip_s from StatiiMaterii sm
	INNER JOIN StatiiDeProcesare s ON sm.cod_s = s.cod_s

select * from StatiiMaterii
select * from vw_StatiiDeProcesare_Active

alter view vw_MateriiPrime_Oua as
	select cod_mp, cod_a from MateriiPrime where nume_mp = 'oua'
select * from vw_MateriiPrime_Oua

select * from materiiprime
--select * from StatiiMaterii
select * from StatiiDeProcesare

select * from materiiprime
select * from animale
select * from SpatiiDeAnimale
insert into animale (specie_a, cod_spatiu, greutate_a) values
('gaina', 1, 3),
('gaina', 1, 4),
('gaina', 1, 2),
('gaina', 1, 3),
('oaie', 2, 10),
('oaie', 2, 8.5),
('oaie', 2, 10.5),
('oaie', 2, 11),
('vaca', 4, 20),
('vaca', 4, 22),
('vaca', 4, 18),
('vaca', 4, 29.5),
('cal', 5, 30),
('cal', 5, 28),
('cal', 5, 27),
('cal', 5, 31),
('rata', 6, 2),
('rata', 6, 3),
('rata', 6, 4),
('rata', 6, 3),
('iepure', 7, 4),
('iepure', 7, 3),
('iepure', 7, 4.5),
('iepure', 7, 3.5)
insert into MateriiPrime (nume_mp, cod_a) values
('oua', 21903),
('oua', 21904),
('oua', 21905),
('oua', 21906),
('carne de oaie', 21907),
('carne de oaie', 21908),
('carne de oaie', 21909),
('carne de oaie', 21910),
('lapte de vaca', 21911),
('lapte de vaca', 21912),
('carne de vita', 21913)
insert into StatiiMaterii (cod_s, cod_mp) values
(1, 22), (1, 23), (1, 24), (1, 25), 
(2, 26), (2, 27), (2, 28), (2, 29),
(4, 30), (4, 31), (2, 32)
insert into MateriiPrime (nume_mp, cod_a) values
('pene', 21903), ('pene', 21904)
insert into StatiiMaterii (cod_s, cod_mp) values
(3, 36), (5, 37)
select * from MateriiPrime
select * from StatiiDeProcesare



