import { PluginListenerHandle } from "@capacitor/core";
import { ConnectionStatus, Network } from "@capacitor/network";
import { useCallback, useEffect, useState } from "react";
import { getLogger } from "../utils";
import { Preferences } from "@capacitor/preferences";

const log = getLogger("useNetwork");

export type NetworkState = {
  connected: boolean;
  connectionType: string;
};

const initialState: NetworkState = {
  connected: true,
  connectionType: "unknown",
};

export const useNetwork = () => {
  const [networkStatus, setNetworkStatus] =
    useState<NetworkState>(initialState);

  useEffect(() => {
    let handler: PluginListenerHandle;

    setInitialNetworkStatus();

    registerNetworkStatusChange();

    let canceled = false;

    return () => {
      canceled = true;
      handler?.remove;
    };

    async function setInitialNetworkStatus() {
      log("setInitialNetworkStatus");
      const status = await Network.getStatus();
      setNetworkStatus(status);
    }

    async function registerNetworkStatusChange() {
      handler = await Network.addListener(
        "networkStatusChange",
        handleNetworkStatusChange
      );
    }
    async function handleNetworkStatusChange(status: ConnectionStatus) {
      console.log("useNetwork - status change", status);
      if (!canceled) {
        setNetworkStatus(status);
      }
    }
  }, []);

  return { networkStatus };
};
