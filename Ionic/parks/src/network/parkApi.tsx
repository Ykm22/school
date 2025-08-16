import axios from "axios";
import { ParkProps } from "../models/Park";
import { getLogger } from "../utils";
import { authConfig } from "../core";

const log = getLogger("parkApi");
const baseUrl = "localhost:3000";
const parkUrl = `http://${baseUrl}/api/parks`;

const config = {
  headers: {
    "Content-Type": "application/json",
  },
};

interface ResponseProps<T> {
  data: T;
}

function withLogs<T>(
  promise: Promise<ResponseProps<T>>,
  fnName: string
): Promise<T> {
  log(`${fnName} - started`);
  return promise
    .then((res) => {
      log(`${fnName} - succeeded`);
      return Promise.resolve(res.data);
    })
    .catch((error) => {
      log(`${fnName} - failed`);
      return Promise.reject(error);
    });
}

export const getParks: (token: string) => Promise<ParkProps[]> = (token) => {
  return withLogs(axios.get(parkUrl, authConfig(token)), "getParks");
};

export const createPark: (
  token: string,
  park: ParkProps
) => Promise<ParkProps> = (token, park) => {
  return withLogs(axios.post(parkUrl, park, authConfig(token)), "createPark");
};

export const updatePark: (
  token: string,
  park: ParkProps
) => Promise<ParkProps> = (token, park) => {
  // !token is empty string on update from ParkEdit
  return withLogs(
    axios.put(`${parkUrl}/${park._id}`, park, authConfig(token)),
    "updatePark"
  );
};

interface MessageData {
  event: string;
  payload: {
    park: ParkProps;
  };
}

export const newWebSocket = (
  token: string,
  onMessage: (data: MessageData) => void
) => {
  const ws = new WebSocket(`ws://${baseUrl}`);
  ws.onopen = () => {
    log("web socket onopen");
    ws.send(JSON.stringify({ type: "authorization", payload: { token } }));
  };

  ws.onclose = () => {
    log("web socket onclose");
  };

  ws.onerror = (error) => {
    log(error);
    log(`web socket onerror, ${error}`);
  };

  ws.onmessage = (messageEvent) => {
    log("web socket onmessage");
    onMessage(JSON.parse(messageEvent.data));
  };

  return () => {
    ws.close();
  };
};
