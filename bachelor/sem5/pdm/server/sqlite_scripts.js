// const sqlite3 = require('sqlite3');

// const db = new sqlite3.Database("db/ParksApp.db", (err) => {
//     if (err) {
//         console.log(err.message);
//     }
//     const insertUserQuery = 'INSERT INTO users (username, password) VALUES (?, ?)';
//     // db.run(insertUserQuery, ["a", "a"]);
//     // db.run(insertUserQuery, ["b", "b"]);
//     const readQuery = `
//       SELECT * FROM USERS
//     `
//     console.log(db.all(readQuery, (err, rows) => {
//       if (err) {
//         console.log(err.message);
//       }
//       console.log(rows);
      
//     }));

//   //   const alterTableQuery = 'PRAGMA foreign_keys=off; \
//   //   BEGIN TRANSACTION; \
//   //   CREATE TABLE parks_backup(_id INTEGER PRIMARY KEY AUTOINCREMENT, userId INTEGER, squared_kms INTEGER, reaches_eco_target BOOLEAN, description TEXT, last_review TEXT); \
//   //   INSERT INTO parks_backup SELECT * FROM parks; \
//   //   DROP TABLE parks; \
//   //   ALTER TABLE parks_backup RENAME TO parks; \
//   //   COMMIT; \
//   //   PRAGMA foreign_keys=on;';

//   // db.exec(alterTableQuery, (err) => {
//   //   if (err) {
//   //     console.error('Error renaming column:', err);
//   //   } else {
//   //     console.log('Column renamed successfully.');
//   //   }
//   db.run(`
//   PRAGMA foreign_keys=off;
//   BEGIN TRANSACTION;
//   ALTER TABLE users RENAME TO old_users;
//   CREATE TABLE IF NOT EXISTS users (
//     _id TEXT PRIMARY KEY,
//     username TEXT,
//     password TEXT
//   );
//   INSERT INTO users (_id, username, password) SELECT _id, username, password FROM old_users;
//   COMMIT;
//   PRAGMA foreign_keys=on;
// `);

// // Alter the parks table to change the _id and userId columns to TEXT
// db.run(`
//   PRAGMA foreign_keys=off;
//   BEGIN TRANSACTION;
//   ALTER TABLE parks RENAME TO old_parks;
//   CREATE TABLE IF NOT EXISTS parks (
//     _id TEXT PRIMARY KEY,
//     userId TEXT,
//     squared_kms INTEGER,
//     reaches_eco_target BOOLEAN,
//     description TEXT,
//     last_review TEXT
//   );
//   INSERT INTO parks (_id, userId, squared_kms, reaches_eco_target, description, last_review)
//   SELECT _id, userId, squared_kms, reaches_eco_target, description, last_review
//   FROM old_parks;
//   COMMIT;
//   PRAGMA foreign_keys=on;
// `);

//     // Close the database connection
//     db.close();
//     console.log("success");
//   //   const createUserTableQuery = `
//   //     CREATE TABLE IF NOT EXISTS users (
//   //       _id INTEGER PRIMARY KEY AUTOINCREMENT,
//   //       username TEXT,
//   //       password TEXT
//   //     )
//   //   `;

//   //    // Create the "parks" table
//   //    const createParksTableQuery = `
//   //    CREATE TABLE IF NOT EXISTS parks (
//   //      _id INTEGER PRIMARY KEY AUTOINCREMENT,
//   //      squared_km INTEGER,
//   //      reaches_eco_target BOOLEAN,
//   //      description TEXT,
//   //      userId INTEGER,
//   //      last_review TEXT
//   //    )
//   //  `;
//    // Execute the table creation queries
//   //  db.run(createUserTableQuery, (err) => {
//   //   if (err) {
//   //     return err.message;
//   //   }

//   //   db.run(createParksTableQuery, (err) => {
//   //     if (err) {
//   //       return err.message;
//   //     }

//   //   });
//   // });
// });



const sqlite3 = require('sqlite3').verbose();

// Open a database connection
const db = new sqlite3.Database('db/ParksApp.db');

// SQL query to add columns to the parks table
const alterTableQuery = `
    PRAGMA foreign_keys=off;
    BEGIN TRANSACTION;

    -- Create a backup of the parks table
    CREATE TABLE parks_backup(_id TEXT, userId TEXT, squared_kms INTEGER, reaches_eco_target BOOLEAN, description TEXT, last_review TEXT);

    -- Copy data from parks to parks_backup
    INSERT INTO parks_backup SELECT * FROM parks;

    -- Drop the existing parks table
    DROP TABLE parks;

    -- Create a new parks table with additional columns
    CREATE TABLE parks (
        _id TEXT,
        userId TEXT,
        squared_kms INTEGER,
        reaches_eco_target BOOLEAN,
        description TEXT,
        last_review TEXT,
        photo_filepath TEXT,
        photo_base64String TEXT,
        photo_webviewPath TEXT
    );

    -- Copy data from parks_backup to the new parks table
    INSERT INTO parks SELECT * FROM parks_backup;

    -- Drop the backup table
    DROP TABLE parks_backup;

    COMMIT;
    PRAGMA foreign_keys=on;
`;

// Execute the query
db.exec(alterTableQuery, (err) => {
    if (err) {
        console.error('Error adding columns:', err);
    } else {
        console.log('Columns added successfully.');
    }

    // Close the database connection
    db.close();
});
