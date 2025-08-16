import axios from "axios";
import { baseUrl, config, withLogs } from "../core";
import { Preferences } from "@capacitor/preferences";
import { getLogger } from "../utils";

const authUrl = `http://${baseUrl}/api/auth/login`;

export interface AuthProps {
  token: string;
}

const log = getLogger("authApi");

const login: (username?: string, password?: string) => Promise<AuthProps> = (
  username,
  password
) => {
  return withLogs(axios.post(authUrl, { username, password }, config), "login");
};

export const obtainToken: (
  username?: string,
  password?: string
) => Promise<AuthProps> = async (username, password) => {
  log("obtainToken");
  const storage_token = await Preferences.get({ key: "jwt" });
  log(`storage_token = ${storage_token}`);
  if (storage_token.value !== null) {
    log(`Found token: ${storage_token.value}`);
    return { token: storage_token.value || "" };
  }

  const { token } = await login(username, password);
  log(`Storing token: ${token}`);
  await Preferences.set({
    key: "jwt",
    value: token,
  });

  return { token };
};
