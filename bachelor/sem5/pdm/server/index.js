const http = require('http');
const Koa = require('koa');
const Router = require('koa-router');
const cors = require('@koa/cors');
const bodyParser = require('koa-bodyparser');
const jwt = require('koa-jwt');
const { jwtConfig, timingLogger, exceptionHandler } = require('./utils.js');
// const WebSocket = require('ws');
const { WebSocketServer } = require('ws');

const { parksRouter } = require('./parksRouter.js');
const { authRouter } = require('./auth.js');

const { initWss } = require('./wss.js');

const app = new Koa();
const server = http.createServer(app.callback());
const wss = new WebSocketServer({ server });
initWss(wss);

app.use(cors());
app.use(timingLogger);
app.use(exceptionHandler);
app.use(bodyParser());

const prefix = '/api';

// public
const publicApiRouter = new Router({ prefix });
publicApiRouter.use('/auth', authRouter.routes());
app
    .use(publicApiRouter.routes())
    .use(publicApiRouter.allowedMethods());

// ! COMMENTED AUTH
// app.use(jwt(jwtConfig));

// protected
const protectedApiRouter = new Router({ prefix });
protectedApiRouter.use('/parks', parksRouter.routes());
app
    .use(protectedApiRouter.routes())
    .use(protectedApiRouter.allowedMethods());

const port = 3000;
console.log(`Running on port: ${port}`);
server.listen(port);