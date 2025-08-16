import { useCallback, useContext, useEffect, useState } from "react";
import { RouteComponentProps } from "react-router";
import { AuthContext } from "./AuthProvider";
import { getLogger } from "../utils";
import {
  IonButton,
  IonCol,
  IonContent,
  IonHeader,
  IonInput,
  IonLoading,
  IonPage,
  IonTitle,
  IonToast,
  IonToolbar,
} from "@ionic/react";

const log = getLogger("Login");

interface LoginState {
  username?: string;
  password?: string;
}

export const Login: React.FC<RouteComponentProps> = ({ history }) => {
  const {
    isAuthenticated,
    isAuthenticating,
    login,
    token_check,
    authenticationError,
    networkStatus,
  } = useContext(AuthContext);
  log(`connected = ${networkStatus.connected}`);

  const [state, setState] = useState<LoginState>({});

  useEffect(() => {
    log("token check callback");
    token_check?.();
  }, []);

  const { username, password } = state;

  const handlePasswordChange = useCallback(
    (e: any) =>
      setState({
        ...state,
        password: e.detail.value || "",
      }),
    [state]
  );

  const handleUsernameChange = useCallback(
    (e: any) =>
      setState({
        ...state,
        username: e.detail.value || "",
      }),
    [state]
  );

  const handleLogin = useCallback(() => {
    log(`handleLogin...xd`);
    login?.(username, password, networkStatus.connected);
  }, [username, password, networkStatus]);

  log("render");
  useEffect(() => {
    if (isAuthenticated) {
      log("redirecting to home");
      history.push("/");
    }
  }, [isAuthenticated]);

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Login</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonInput
          placeholder="Username"
          value={username}
          onIonChange={handleUsernameChange}
        />
        <IonInput
          placeholder="Password"
          value={password}
          onIonChange={handlePasswordChange}
        />
        <IonLoading isOpen={isAuthenticating} />
        {authenticationError && (
          <div>{authenticationError.message || "Filaed to authenticate"}</div>
        )}
        <IonButton onClick={handleLogin}>Login</IonButton>
      </IonContent>
    </IonPage>
  );
};
