const Router = require('koa-router');
const { broadcast } = require('./wss.js');
const { dbFilePath } = require('./utils.js');
const sqlite3 = require('sqlite3');
const { v4: uuidv4 } = require('uuid');

class ParkStore {
    constructor() {}

    async connect() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(dbFilePath, (err) => {
                if (err) {
                    return reject(err);
                }
                resolve();
            })
        });
    }

    async find({ userId }) {
        return new Promise((resolve, reject) => {
            const query = `
                SELECT * FROM parks
                WHERE userId = ?
            `;
            this.db.all(query, [userId], (err, rows) => {
                if (err) {
                    reject(err);
                }
                const modified_rows = rows.map(row => {
                    return {
                        _id: row._id,
                        userId: row.userId,
                        squared_kms: row.squared_kms,
                        reaches_eco_target: row.reaches_eco_target,
                        description: row.description,
                        last_review: row.last_review,
                        photo: {
                            filepath: row.photo_filepath,
                            webviewPath: row.photo_webviewPath,
                            base64String: row.photo_base64String,
                        },
                        coordinates: {
                            lat: row.coordinates_lat,
                            lng: row.coordinates_lng,
                        },
                    };
                });
                resolve(modified_rows);
            })
        })
    }

    async findOne({ _id }) {
        return new Promise((resolve, reject) => {
            const query = "SELECT * FROM parks WHERE _id = ?";
            this.db.get(query, [_id], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            })
        })
    }

    async insert({description, squared_kms, last_review, reaches_eco_target, userId, photo, coordinates}) {
        if(!description) {
            throw new Error("Missing description");
        }
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO parks 
                (
                    _id, 
                    userId, 
                    squared_kms,
                    reaches_eco_target, 
                    description, 
                    last_review, 
                    photo_filepath, 
                    photo_webviewPath, 
                    photo_base64String,
                    coordinates_lat,
                    coordinates_lng,
                )
                VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `;
            const _id = uuidv4();
            this.db.run(query, [_id, 
                userId, 
                squared_kms, 
                reaches_eco_target, 
                description, 
                last_review,
                photo.filepath, 
                photo.webviewPath, 
                photo.base64String,
                coordinates.lat,
                coordinates.lng,
            ], (err) => {
                if(err) {
                    reject(err);
                } else {
                    resolve({
                        _id,
                        description,
                        squared_kms,
                        last_review,
                        reaches_eco_target,
                        userId,
                        photo,
                        coordinates,
                    });
                }
            });
        });
    }

    async update({ _id }, park) {
        // console.log(park)
        // console.log(typeof(park.coordinates.lat));
        return new Promise((resolve, reject) => {
            const query = `
                UPDATE parks
                SET squared_kms = ?, 
                    reaches_eco_target = ?, 
                    description = ?, 
                    last_review = ?,
                    photo_filepath = ?,
                    photo_webviewPath = ?,
                    photo_base64String = ?,
                    coordinates_lat = ?,
                    coordinates_lng = ?
                WHERE _id = ?
            `;
            this.db.run(query, 
                [park.squared_kms, 
                park.reaches_eco_target, 
                park.description, 
                park.last_review, 
                park.photo.filepath,
                park.photo.webviewPath,
                park.photo.base64String,
                park.coordinates.lat,
                park.coordinates.lng,
                _id,
            ], (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(1); // rows affected
                }
            })
        })
    }

    async remove({ _id }) {
        return new Promise((resolve, reject) => {
            const query = `
                DELETE FROM parks
                WHERE _id = ?
            `;
            this.db.run(query, [_id], (err) => {
                if (err) {
                    reject(err);
                } else { 
                    resolve();
                }
            })
        })
    }
}

const parkStore = new ParkStore();

const parksRouter = new Router();

parksRouter.get('/', async (ctx) => {
    // const userId = ctx.state.user._id;
    const userId = "1";
    // console.log(userId);
    await parkStore.connect();

    ctx.response.body = await parkStore.find({ userId });
    // console.log(ctx.response.body);
    // console.log(await parkStore.find({ userId }));
    ctx.response.status = 200;
});

parksRouter.get('/:id', async (ctx) => {
    const userId = ctx.state.user._id;
    await parkStore.connect();

    const park = await parkStore.findOne({ _id: ctx.params.id });
    const response = ctx.response;

    if (park) {
        if (park.userId === userId) {
            ctx.response.body = park;
            ctx.response.status = 200;
        } else {
            ctx.response.status = 403; // FORBIDDEN
        }
    } else {
        ctx.response.status = 404; // NOT FOUND
    }
});

const createPark = async (ctx, park, response) => {
    try {
        const userId = ctx.state.user._id;
        park.userId = userId;
        await parkStore.connect();
        // console.log(park.coordinates);
        const inserted_park = await parkStore.insert(park);
        response.body = inserted_park;
        response.status = 201; // created
        broadcast(userId, { event: 'created', payload: { park: inserted_park} });
    } catch (err) {
        response.body = { message: err.message };
        response.status = 400; // bad request
    }
};

parksRouter.post('/', async ctx => await createPark(ctx, ctx.request.body, ctx.response));

parksRouter.put('/:id', async ctx => {
    const park = ctx.request.body;
    console.log(park);
    const id = ctx.params.id;
    const parkId = park._id;
    const response = ctx.response;
    if (parkId && parkId !== id) {
        response.body = { message: 'Param id and body _id should be the same' };
        response.status = 400;
        return;
    }
    await parkStore.connect();
    if (!parkId) {
        await createPark(ctx, park, response);
    } else {
        // const userId = ctx.state.user._id;
        const userId = "1";
        park.userId = userId;
        const updatedCount = await parkStore.update({_id: id }, park);
        park._id = id;
        if(updatedCount === 1) {
            response.body = park;
            response.status = 200;
            // console.log("in put parks.js");
            // console.log(park);
            broadcast(userId, { event: 'updated', payload: { park: park } });
        } else {
            response.body = { message: 'Resource no longer exists' };
            response.status = 405; // METHOD NOT ALLOWED
        }
    }
});

parksRouter.del('/:id', async (ctx) => {
    const userId = ctx.state.user._id;
    await parkStore.connect();
    const park = await parkStore.findOne({ _id: ctx.params.id });
    
    if (park && userId !== park.userId) {
        ctx.response.status = 403;
    } else {
        await parkStore.remove({ _id: ctx.params.id });
        ctx.response.status = 204; // NO CONTENT
    }
});

module.exports = { parksRouter };