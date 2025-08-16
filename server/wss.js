const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
const { jwtConfig } = require('./utils.js');

let wss;

const initWss = value => {
  wss = value;
  wss.on('connection', ws => {
    ws.on('message', message => {
      const { type, payload: { token } } = JSON.parse(message);
      if (type !== 'authorization') {
        ws.close();
        return;
      }
      try {
        ws.user = jwt.verify(token, jwtConfig.secret);
      } catch (err) {
        ws.close();
      }
    })
  });
};

const broadcast = (userId, data) => {
  if (!wss) {
    return;
  }
  // console.log("broadcast");
  // console.log(data);
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN && userId === client.user._id) {
      console.log(`broadcast sent to ${client.user.username}`);
      client.send(JSON.stringify(data));
    }
  });
};

module.exports = { initWss, broadcast };
