import { getLogger } from "../core";
import { useCamera } from "./useCamera";
import { useFilesystem } from "./useFilesystem";

const log = getLogger("usePhotos");

export interface MyPhoto {
  filepath: string;
  webviewPath?: string;
  base64String?: string;
}

export function usePhotos() {
  const { getPhoto } = useCamera();
  const { readFile, writeFile, deleteFile } = useFilesystem();

  async function takePhoto() {
    log("takePhoto");
    const { base64String } = await getPhoto();
    const filepath = new Date().getTime() + ".jpeg";

    await writeFile(filepath, base64String!);

    const webviewPath = `data:image/jpeg;base64,${base64String}`;
    const newPhoto = { filepath, webviewPath, base64String };

    return newPhoto;
  }
  return {
    takePhoto,
  };
}
