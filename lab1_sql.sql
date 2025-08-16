CREATE TABLE SpatiiDeAnimale(
cod_spatiu INT PRIMARY KEY IDENTITY,
nr_spatiu INT,
nrMaximAnimale_spatiu INT,
tip_spatiu VARCHAR(100)
);
CREATE TABLE Animale(
cod_a INT PRIMARY KEY IDENTITY,
specie_a VARCHAR(100),
descriere_a VARCHAR(100),
cod_spatiu INT FOREIGN KEY REFERENCES SpatiiDeAnimale(cod_spatiu) ON UPDATE CASCADE ON DELETE CASCADE
);  
CREATE TABLE Furaje(
cod_f INT PRIMARY KEY IDENTITY,
nume_f VARCHAR(100),
cantitate_f INT CHECK (cantitate_f >= 0)
);
CREATE TABLE AnimaleFuraje(
cod_a INT,
cod_f INT,
CONSTRAINT fk_Animale FOREIGN KEY (cod_a) REFERENCES Animale(cod_a),
CONSTRAINT fk_Furaje FOREIGN KEY (cod_f) REFERENCES Furaje(cod_f),
CONSTRAINT pk_AnimaleFuraje PRIMARY KEY (cod_a, cod_f)
);
CREATE TABLE Ingrijitori(
cod_i INT PRIMARY KEY IDENTITY,
nume_i VARCHAR(100),
salariu_i INT CHECK(salariu_i > 0),
ore_i INT CHECK(ore_i >= 0),
cod_spatiu INT FOREIGN KEY REFERENCES SpatiiDeAnimale(cod_spatiu) ON UPDATE CASCADE ON DELETE CASCADE,
);
CREATE TABLE MateriiPrime(
cod_mp INT PRIMARY KEY IDENTITY,
nume_mp VARCHAR(100),
cod_a INT FOREIGN KEY REFERENCES Animale(cod_a) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE StatiiDeProcesare(
cod_s INT PRIMARY KEY IDENTITY,
tip_s VARCHAR(100)
);
CREATE TABLE Muncitori(
cod_m INT PRIMARY KEY IDENTITY,
nume_m VARCHAR(100),
salariu_m INT CHECK(salariu_m > 0),
ore_m INT CHECK(ore_m >= 0),
cod_s INT FOREIGN KEY REFERENCES StatiiDeProcesare(cod_s) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE Magazin(
cod_mag INT PRIMARY KEY IDENTITY,
nume_mag VARCHAR(100),
castig_mag INT CHECK(castig_mag >= 0)
);
CREATE TABLE StatiiMaterii(
cod_s INT,
cod_mp INT,
CONSTRAINT fk_Statii FOREIGN KEY (cod_s) REFERENCES StatiiDeProcesare(cod_s),
CONSTRAINT fk_Materii FOREIGN KEY (cod_mp) REFERENCES MateriiPrime(cod_mp),
CONSTRAINT pk_StatiiMaterii PRIMARY KEY (cod_s, cod_mp)
);
CREATE TABLE ProduseFinite(
cod_pf INT PRIMARY KEY IDENTITY,
nume_pf VARCHAR(100),
cod_mag INT FOREIGN KEY REFERENCES Magazin(cod_mag) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE StatiiProduse(
cod_s INT,
cod_pf INT,
CONSTRAINT fk_StatiiP FOREIGN KEY (cod_s) REFERENCES StatiiDeProcesare(cod_s),
CONSTRAINT fk_ProduseS FOREIGN KEY (cod_pf) REFERENCES ProduseFinite(cod_pf),
CONSTRAINT pk_StatiiProduse PRIMARY KEY (cod_s, cod_pf)
);