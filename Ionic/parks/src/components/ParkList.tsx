import {
  IonButton,
  IonCheckbox,
  IonContent,
  IonFab,
  IonFabButton,
  IonHeader,
  IonIcon,
  IonInfiniteScroll,
  IonInfiniteScrollContent,
  IonInput,
  IonItem,
  IonItemDivider,
  IonLabel,
  IonList,
  IonLoading,
  IonPage,
  IonSearchbar,
  IonTitle,
  IonToolbar,
} from "@ionic/react";
import { add, checkmarkCircle, closeCircle } from "ionicons/icons";
import React, { useContext } from "react";
import Park from "../models/Park";
import { getLogger } from "../utils";
import { ParkContext } from "../contexts/ParkProvider";
import { RouteComponentProps } from "react-router";
import { Preferences } from "@capacitor/preferences";
import "./style.css";

const log = getLogger("ParkList");

const ParkList: React.FC<RouteComponentProps> = ({ history }) => {
  const {
    parks,
    fetching,
    fetchingError,
    handleLogout,
    networkStatus,
    loadNextPage,
    handleSearchInput,
    handleEcoFriendlyFilter,
  } = useContext(ParkContext);

  log("render");
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle slot="start">ParkSeein'</IonTitle>
          <div className="scrolling-text-container">
            {networkStatus?.connected ? (
              <>
                <IonIcon
                  icon={checkmarkCircle}
                  color="success"
                  className="scrolling-text"
                />
                <IonLabel color="success" className="scrolling-text">
                  Online
                </IonLabel>
              </>
            ) : (
              <>
                <IonIcon
                  icon={closeCircle}
                  color="danger"
                  className="scrolling-text"
                />
                <IonLabel color="danger" className="scrolling-text">
                  Offline
                </IonLabel>
              </>
            )}
          </div>
          <IonButton slot="end" onClick={handleLogout}>
            Logout
          </IonButton>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonLoading isOpen={fetching} message="Loading parks" />
        <IonSearchbar
          placeholder="Search parks"
          debounce={1000}
          onIonInput={(ev) => {
            if (handleSearchInput) {
              handleSearchInput(ev);
            }
          }}
        />
        <IonItem>
          {/* <IonLabel>Eco friendly </IonLabel> */}
          <IonCheckbox
            onIonChange={(ev) => {
              if (handleEcoFriendlyFilter) {
                handleEcoFriendlyFilter(ev);
              }
            }}
          >
            Reaches Eco Target
          </IonCheckbox>
        </IonItem>
        <IonItemDivider />
        {parks && (
          <IonList>
            {parks.map(
              ({
                _id,
                description,
                squared_kms,
                last_review,
                reaches_eco_target,
                photo,
                coordinates,
              }) => (
                <Park
                  key={_id}
                  _id={_id}
                  description={description}
                  squared_kms={squared_kms}
                  last_review={last_review}
                  reaches_eco_target={reaches_eco_target}
                  photo={photo}
                  coordinates={coordinates}
                  onEdit={(id) => history.push(`/park/${id}`)}
                />
              )
            )}
          </IonList>
        )}
        <IonInfiniteScroll
          onIonInfinite={(ev) => {
            if (loadNextPage) {
              loadNextPage();
              setTimeout(() => ev.target.complete(), 500);
            }
          }}
        >
          <IonInfiniteScrollContent></IonInfiniteScrollContent>
        </IonInfiniteScroll>
        {fetchingError && (
          <div>{fetchingError.message || "Failed to load parks"}</div>
        )}
        <IonFab vertical="bottom" horizontal="end" slot="fixed">
          <IonFabButton onClick={() => history.push("/park")}>
            <IonIcon icon={add} />
          </IonFabButton>
        </IonFab>
      </IonContent>
    </IonPage>
  );
};

export default ParkList;
