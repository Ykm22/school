import {
  Photo,
  Camera,
  CameraResultType,
  CameraSource,
} from "@capacitor/camera";
import { useCallback } from "react";
import { getLogger } from "../core";

const log = getLogger("useCamera");

export function useCamera() {
  const getPhoto = useCallback<() => Promise<Photo>>(() => {
    log("getPhoto");
    return Camera.getPhoto({
      resultType: CameraResultType.Base64,
      source: CameraSource.Camera,
      quality: 20,
    });
  }, []);

  return {
    getPhoto,
  };
}
