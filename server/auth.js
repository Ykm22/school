const { jwtConfig, dbFilePath } = require('./utils.js');
const Router = require('koa-router');
const jwt = require('jsonwebtoken');
const sqlite3 = require('sqlite3');

class UserStore {
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

    async findOne({ username }) {
        return new Promise((resolve, reject) => {
            const query = "SELECT * FROM users WHERE username = ?";
            this.db.get(query, [username], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            })
        })
    }

    async insert({ username, password}) {
        return new Promise((resolve, reject) => {
            const query = `
                INSERT INTO users (username, password)
                VALUES (?, ?)
            `;
            this.db.run(query, [username, password], (err) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(this.lastId);
                }
            })
        })
    }

    close() {
        if (this.db) {
            this.db.close();
        }
    }
}

const userStore = new UserStore();

const createToken = (user) => {
    return jwt.sign(
        { 
            username: user.username, 
            _id: user._id 
        }, 
        jwtConfig.secret, 
        { expiresIn: 60 * 60 * 60 }
    );
}

const authRouter = new Router();

authRouter.post('/signup', async (ctx) => {
    try {
        const user = ctx.request.body;
        await userStore.connect();
        await userStore.insert(user);
        ctx.response.body = { token: createToken(user) };
        ctx.response.status = 201; // created
      } catch (err) {
        ctx.response.body = { error: err.message };
        ctx.response.status = 400; // bad request
      }
    
      await createUser(ctx.request.body, ctx.response)
});

authRouter.post('/login', async (ctx) => {
    try {
        const credentials = ctx.request.body;
        await userStore.connect();
        const user = await userStore.findOne({ username: credentials.username });
        if (user && credentials.password === user.password) {
          ctx.response.body = { token: createToken(user) };
          ctx.response.status = 201; // created
        } else {
          ctx.response.body = { error: 'Invalid credentials' };
          ctx.response.status = 400; // bad request
        }
    } catch (error) {
        console.error('Error: ', error);
    } finally {
        userStore.close();
    }
});

module.exports = { authRouter };