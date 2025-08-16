import React, { createContext, useCallback, useEffect, useState } from "react";
import { getLogger } from "../utils";
import PropTypes from "prop-types";
import { obtainToken } from "./authApi";
import { Preferences } from "@capacitor/preferences";
import { NetworkState, useNetwork } from "../network/useNetwork";

const log = getLogger("AuthProvider");

type LoginFn = (
  username?: string,
  password?: string,
  connected?: boolean
) => void;
type TokenCheckFn = () => void;
export type HandleLogoutFn = () => void;

export interface AuthState {
  authenticationError: Error | null;
  isAuthenticated: boolean;
  isAuthenticating: boolean;
  login?: LoginFn;
  pendingAuthentication?: boolean;
  username?: string;
  password?: string;
  token: string;
  token_check?: TokenCheckFn;
  handleLogout?: HandleLogoutFn;
  networkStatus: NetworkState;
}

const initialState: AuthState = {
  isAuthenticated: false,
  isAuthenticating: false,
  authenticationError: null,
  pendingAuthentication: false,
  token: "",
  networkStatus: {
    connected: true,
    connectionType: "unknown",
  },
};

export const AuthContext = createContext<AuthState>(initialState);

interface AuthProviderProps {
  children: PropTypes.ReactNodeLike;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, setState] = useState<AuthState>(initialState);
  const {
    isAuthenticated,
    isAuthenticating,
    authenticationError,
    pendingAuthentication,
    token,
  } = state;

  const token_check = () => {
    log("token check");
    checkToken();

    async function checkToken() {
      try {
        const result = await Preferences.get({ key: "jwt" });
        if (result.value) {
          setState({
            ...state,
            isAuthenticated: true,
            token: result.value,
          });
        }
      } catch (err) {
        log(`Error fetching checking token ${err}`);
      }
    }
  };

  const login = useCallback<LoginFn>(loginCallback, []);
  useEffect(authenticationEffect, [pendingAuthentication]);

  function handleLogout() {
    log("logging out");
    logout();

    async function logout() {
      try {
        const result = await Preferences.get({ key: "jwt" });
        await Preferences.remove({ key: "jwt" });
        await Preferences.remove({ key: "parks" });
        if (result.value) {
          setState({
            ...state,
            isAuthenticated: false,
            pendingAuthentication: false,
            token: "",
          });
        }
      } catch (err) {
        log("error in logout");
      }
    }
  }

  const { networkStatus } = useNetwork();
  const value = {
    isAuthenticated,
    login,
    isAuthenticating,
    authenticationError,
    token,
    token_check,
    handleLogout,
    networkStatus,
  };
  log("render");
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;

  function loginCallback(
    username?: string,
    password?: string,
    connected?: boolean
  ): void {
    log("login");
    if (!connected) {
      setState({
        ...state,
        authenticationError: {
          name: "InternetError",
          message: "No internet connection",
        },
      });
    } else {
      setState({
        ...state,
        pendingAuthentication: true,
        username,
        password,
      });
    }
  }

  function authenticationEffect() {
    let canceled = false;
    authenticate();
    return () => {
      canceled = true;
    };

    async function authenticate() {
      if (!pendingAuthentication) {
        log("authenticate, !pendingAuthentication, return");
        return;
      }
      try {
        log("authenticate...");
        setState({
          ...state,
          isAuthenticating: true,
        });
        const { username, password } = state;
        const { token } = await obtainToken(username, password);
        if (canceled) {
          return;
        }
        log("authenticate succeeded");
        setState({
          ...state,
          token,
          pendingAuthentication: false,
          isAuthenticated: true,
          isAuthenticating: false,
        });
      } catch (error) {
        if (canceled) {
          return;
        }
        log("authenticate failed");
        setState({
          ...state,
          authenticationError: error as Error,
          pendingAuthentication: false,
          isAuthenticating: false,
        });
      }
    }
  }
};
