import {
  IonButton,
  IonButtons,
  IonContent,
  IonDatetime,
  IonHeader,
  IonModal,
  IonTitle,
  IonToolbar,
  createAnimation,
} from "@ionic/react";
import { MyDatepickerModal } from "./ParkEdit";

export const MyModal: React.FC<MyDatepickerModal> = ({
  last_review,
  setShowDatepicker,
  handleDateSelection,
  showDatePicker,
}) => {
  const enterAnimation = (baseEl: any) => {
    const root = baseEl.shadowRoot;
    const backdropAnimation = createAnimation()
      .addElement(root.querySelector("ion-backdrop")!)
      .fromTo("opacity", "0.01", "var(--backdrop-opacity)");

    const wrapperAnimation = createAnimation()
      .addElement(root.querySelector(".modal-wrapper")!)
      .keyframes([
        { offset: 0, opacity: "0", transform: "scale(0)" },
        { offset: 1, opacity: "0.99", transform: "scale(1)" },
      ]);

    return createAnimation()
      .addElement(baseEl)
      .easing("ease-out")
      .duration(500)
      .addAnimation([backdropAnimation, wrapperAnimation]);
  };

  const leaveAnimation = (baseEl: any) => {
    return enterAnimation(baseEl).direction("reverse");
  };

  return (
    <>
      <IonModal
        isOpen={showDatePicker}
        enterAnimation={enterAnimation}
        leaveAnimation={leaveAnimation}
      >
        <IonHeader>
          <IonToolbar>
            <IonTitle>Select a Date</IonTitle>
            <IonButtons slot="end">
              <IonButton onClick={() => setShowDatepicker(false)}>
                Close
              </IonButton>
            </IonButtons>
          </IonToolbar>
        </IonHeader>
        <IonContent>
          <IonDatetime
            onIonChange={(e) => handleDateSelection(String(e.detail.value))}
            value={last_review.toISOString()}
          ></IonDatetime>
        </IonContent>
      </IonModal>
    </>
  );
};
