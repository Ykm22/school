import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useReducer,
} from "react";
import { ParkProps } from "../models/Park";
import PropTypes from "prop-types";
import { getLogger } from "../utils";
import {
  getParks,
  updatePark,
  createPark,
  newWebSocket,
} from "../network/parkApi";
import { AuthContext, HandleLogoutFn } from "../auth";
import { Preferences } from "@capacitor/preferences";
import { NetworkState, useNetwork } from "../network/useNetwork";
import {
  CheckboxChangeEventDetail,
  InputChangeEventDetail,
  useIonToast,
} from "@ionic/react";
import uuid from "uuid-random";
import { returnUpBackOutline } from "ionicons/icons";

const log = getLogger("ParkProvider");

type SaveParkFn = (park: ParkProps) => Promise<any>;

export interface ParksState {
  parks?: ParkProps[];
  fetching: boolean;
  fetchingError?: Error | null;
  saving: boolean;
  savingError?: Error | null;
  savePark?: SaveParkFn;
  handleLogout?: HandleLogoutFn;
  networkStatus?: NetworkState;
  loadNextPage?: () => void;
  handleSearchInput?: (ev: CustomEvent<InputChangeEventDetail>) => void;
  handleEcoFriendlyFilter?: (
    ev: CustomEvent<CheckboxChangeEventDetail>
  ) => void;
}

const initialState: ParksState = {
  fetching: false,
  saving: false,
};

export const ParkContext = createContext<ParksState>(initialState);

interface ParkProviderProps {
  children: PropTypes.ReactNodeLike;
}

interface ActionProps {
  type: string;
  payload?: any;
}

const FETCH_PARKS_STARTED = "FETCH_PARKS_STARTED";
const FETCH_PARKS_SUCCEEDED = "FETCH_PARKS_SUCCEEDED";
const FETCH_PARKS_FAILED = "FETCH_PARKS_FAILED";
const SAVE_PARK_STARTED = "SAVE_PARK_STARTED";
const SAVE_PARK_SUCCEEDED = "SAVE_PARK_SUCCEEDED";
const SAVE_PARK_FAILED = "SAVE_PARK_FAILED";

const reducer: (state: ParksState, action: ActionProps) => ParksState = (
  state,
  { type, payload }
) => {
  switch (type) {
    case FETCH_PARKS_STARTED:
      return { ...state, fetching: true, fetchingError: null };
    case FETCH_PARKS_SUCCEEDED:
      return { ...state, fetching: false, parks: payload.parks };
    case FETCH_PARKS_FAILED:
      return { ...state, fetching: false, fetchingError: payload.error };
    case SAVE_PARK_STARTED:
      return { ...state, saving: true, savingError: null };
    case SAVE_PARK_SUCCEEDED:
      const parks = [...(state.parks || [])];
      const saved_park = payload.park;
      log(`saved_park_id = ${saved_park._id}`);
      const index = parks.findIndex((park) => park._id === saved_park._id);
      if (index === -1) {
        parks.splice(0, 0, saved_park);
      } else {
        parks[index] = saved_park;
      }
      return { ...state, saving: false, parks };
    case SAVE_PARK_FAILED:
      return { ...state, saving: false, savingError: payload.error };
    default:
      return state;
  }
};

export const ParkProvider: React.FC<ParkProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const { parks, fetching, fetchingError, saving, savingError } = state;

  const { token, handleLogout, networkStatus } = useContext(AuthContext);
  const [presentToast] = useIonToast();

  useEffect(getParksEffect, [token, networkStatus]);
  useEffect(wsEffect, [token]);
  useEffect(connectionChangeEffect, [token, networkStatus]);

  const savePark = useCallback<SaveParkFn>(saveParkCallback, [
    token,
    networkStatus,
    presentToast,
  ]);

  const loadNextPage = async () => {
    log("loadNextPage");
    const current_page = await Preferences.get({ key: "current_page" });
    if (!current_page.value) {
      log("No current page value in Preferences");
      return;
    }

    const parks_result = await Preferences.get({ key: "display_parks" });
    if (!parks_result.value) {
      log("No parks value in Preferences");
      return;
    }
    const parks = JSON.parse(parks_result.value);

    const next_page = parseInt(current_page.value) + 1;
    log(`Current_page = ${next_page}`);

    dispatch({
      type: FETCH_PARKS_SUCCEEDED,
      payload: {
        parks: parks.slice(0, next_page * 10),
      },
    });

    await Preferences.set({
      key: "current_page",
      value: next_page.toString(),
    });
  };

  const handleSearchInput = async (ev: CustomEvent<InputChangeEventDetail>) => {
    const parks_result = await Preferences.get({ key: "parks" });
    if (!parks_result.value) {
      return;
    }
    const parks = JSON.parse(parks_result.value);
    const filtered_parks = parks.filter(
      (park: {
        description: { startsWith: (arg0: string | null | undefined) => any };
      }) => park.description.startsWith(ev.detail.value)
    );
    dispatch({
      type: FETCH_PARKS_SUCCEEDED,
      payload: { parks: filtered_parks.slice(0, 10) },
    });
    await Preferences.set({
      key: "display_parks",
      value: JSON.stringify(filtered_parks),
    });
    await Preferences.set({ key: "current_page", value: "1" });
  };

  const handleEcoFriendlyFilter = async (
    ev: CustomEvent<CheckboxChangeEventDetail>
  ) => {
    log("handleEcoFriendlyFilter");
    const parks_result = await Preferences.get({ key: "parks" });
    if (!parks_result.value) {
      log("no parks locally stored");
      return;
    }
    log("found parks stored locally");
    const parks = JSON.parse(parks_result.value);
    const isEcoFriendly = ev.detail.checked;
    log(`is eco friendly from checkbox: ${isEcoFriendly}`);
    const filtered_parks = parks.filter(
      (park: { reaches_eco_target: boolean }) =>
        park.reaches_eco_target == isEcoFriendly
    );
    dispatch({
      type: FETCH_PARKS_SUCCEEDED,
      payload: { parks: filtered_parks.slice(0, 10) },
    });
    await Preferences.set({
      key: "display_parks",
      value: JSON.stringify(filtered_parks),
    });
    await Preferences.set({ key: "current_page", value: "1" });
  };

  const value = {
    parks,
    fetching,
    fetchingError,
    saving,
    savingError,
    savePark,
    handleLogout,
    networkStatus,
    loadNextPage,
    handleSearchInput,
    handleEcoFriendlyFilter,
  };
  log("returns");

  return <ParkContext.Provider value={value}>{children}</ParkContext.Provider>;

  function getParksEffect() {
    let canceled = false;
    if (token) {
      log("fetching parks");
      loadParks(networkStatus);
    }

    return () => {
      canceled = true;
    };

    async function loadParks(networkStatus: NetworkState) {
      if (!networkStatus.connected) {
        fetchParksStorage();
      } else {
        fetchParksServer();
      }
    }

    async function fetchParksStorage() {
      log("fetchParksStorage");
      const result = await Preferences.get({ key: "parks" });
      if (result.value) {
        log("fetchParksStorage succeeded");
        const parks = JSON.parse(result.value);
        await Preferences.set({ key: "current_page", value: "1" });
        dispatch({
          type: FETCH_PARKS_SUCCEEDED,
          payload: { parks: parks.slice(0, 10) },
        });
      }
    }

    async function fetchParksServer() {
      try {
        log("fetchParksServer");
        dispatch({ type: FETCH_PARKS_STARTED });
        const parks = await getParks(token);
        log("fetchParksServer succeeded");
        if (!canceled) {
          parks.forEach(
            (park) => (park.last_review = new Date(park.last_review))
          );
          await Preferences.set({
            key: "parks",
            value: JSON.stringify(parks),
          });
          await Preferences.set({
            key: "display_parks",
            value: JSON.stringify(parks),
          });
          await Preferences.set({ key: "current_page", value: "1" });
          dispatch({
            type: FETCH_PARKS_SUCCEEDED,
            payload: { parks: parks.slice(0, 10) },
          });
        }
      } catch (error) {
        log("fetchParksServer failed");
        if (!canceled) {
          dispatch({ type: FETCH_PARKS_FAILED, payload: { error } });
        }
      }
    }
  }

  async function saveParkCallback(park: ParkProps) {
    try {
      log("saveParkCallback");
      if (!networkStatus.connected) {
        log("no internet connection");

        presentToast({
          message: "Data not saved.. waiting connection.. 😟",
          duration: 2000,
          color: "danger",
          position: "top",
        });

        const queue_result = await Preferences.get({ key: "queue" });
        let queue;
        if (queue_result.value) {
          queue = JSON.parse(queue_result.value);
        } else {
          queue = [];
        }
        let operation = {
          park,
          type: "unknown",
        };
        if (park._id) {
          operation.type = "update";
        } else {
          operation.type = "save";
          operation.park._id = uuid();
        }
        queue.push(operation);

        await Preferences.remove({ key: "queue" });
        await Preferences.set({ key: "queue", value: JSON.stringify(queue) });

        dispatch({ type: SAVE_PARK_SUCCEEDED, payload: { park } });
      } else {
        log("savePark started");
        dispatch({ type: SAVE_PARK_STARTED });
        const savedPark = await (park._id
          ? updatePark(token, park)
          : createPark(token, park));
        log("savePark succeeded");
        dispatch({ type: SAVE_PARK_SUCCEEDED, payload: { park: savedPark } });
      }
    } catch (error) {
      log("savePark failed");
      dispatch({ type: SAVE_PARK_FAILED, payload: { error } });
    }
  }

  function wsEffect() {
    let canceled = false;
    log("wsEffect - connecting");
    let closeWebSocket: () => void;
    if (token?.trim()) {
      closeWebSocket = newWebSocket(token, (message) => {
        if (canceled) {
          return;
        }

        const {
          event,
          payload: { park },
        } = message;
        log(`ws message, park ${event}`);

        if (event === "created" || event === "updated") {
          dispatch({ type: SAVE_PARK_SUCCEEDED, payload: { park } });
        }
      });
    }

    return () => {
      log("wsEffect - disconnecting");
      canceled = true;
      closeWebSocket?.();
    };
  }

  function connectionChangeEffect() {
    let canceled = false;

    log("connectionChangeEffect");
    if (!networkStatus.connected) {
      log("no connection");
      return;
    }

    log("internet connection");
    makeOfflineChanges();

    async function makeOfflineChanges() {
      const queue_result = await Preferences.get({ key: "queue" });
      if (queue_result.value) {
        log("got offline changes");
        const queue = JSON.parse(queue_result.value);

        try {
          for (let i = 0; i < queue.length; i++) {
            const { park, type } = queue[i];
            if (type === "save") {
              dispatch({ type: SAVE_PARK_STARTED });
              const savedPark = await createPark(token, park);

              const placeholder_id = park._id;
              const server_id = savedPark._id;
              for (let j = i + 1; j < queue.length; j++) {
                const { park } = queue[j];
                if (park._id === placeholder_id) {
                  park._id = server_id;
                }
              }

              dispatch({
                type: SAVE_PARK_SUCCEEDED,
                payload: { park: savedPark },
              });
            } else if (type === "update") {
              dispatch({ type: SAVE_PARK_STARTED });
              const savedPark = await updatePark(token, park);
              dispatch({
                type: SAVE_PARK_SUCCEEDED,
                payload: { park: savedPark },
              });
            } else {
              log("unknown operation");
            }
          }
          presentToast({
            message: "All changes now saved! 😊",
            duration: 2000,
            color: "success",
            position: "top",
          });
          await Preferences.remove({ key: "queue" });
        } catch (error) {
          log("offline operations failed");
          dispatch({ type: SAVE_PARK_FAILED, payload: { error } });
        }
      }
    }

    return () => {
      canceled = true;
    };
  }
};
