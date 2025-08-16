const jwtConfig = { secret: 'my-secret' };

const exceptionHandler = async (ctx, next) => {
  try {
    return await next();
  } catch (err) {
    console.log(err);
    ctx.body = { message: err.message || 'Unexpected error.' };
    ctx.status = err.status || 500;
  }
};

const timingLogger = async (ctx, next) => {
  const start = Date.now();
  await next();
  console.log(`${ctx.method} ${ctx.url} => ${ctx.response.status}, ${Date.now() - start}ms`);
};

const dbFilePath = './db/ParksApp.db';

module.exports = { jwtConfig, exceptionHandler, timingLogger, dbFilePath };