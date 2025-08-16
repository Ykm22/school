import { IonItem, IonLabel } from "@ionic/react";
import React, { memo } from "react";
import { MyPhoto } from "../custom_hooks/usePhotos";
import { MarkerCoordinates } from "../components/MyMap";

export interface ParkProps {
  _id?: string;
  description: string;
  squared_kms: number;
  last_review: Date;
  reaches_eco_target: boolean;
  photo: MyPhoto;
  coordinates: MarkerCoordinates;
}

interface ParkPropsExt extends ParkProps {
  onEdit: (_id?: string) => void;
}

const Park: React.FC<ParkPropsExt> = ({
  _id,
  description,
  squared_kms,
  last_review,
  reaches_eco_target,
  onEdit,
}) => {
  return (
    <IonItem onClick={() => onEdit(_id)}>
      <IonLabel>{description}</IonLabel>
    </IonItem>
  );
};

export default memo(Park);
