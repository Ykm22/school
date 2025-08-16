import { GoogleMap } from "@capacitor/google-maps";
import { useEffect, useRef, useState } from "react";
import { mapsApiKey } from "../core/mapsApiKey";
import { getLogger } from "../core";
import { myMapRef } from "./ParkEdit";

const log = getLogger("MyMap");

interface MyMapProps {
  lat: number;
  lng: number;
  setCoordinates: (markerCoordinates: MarkerCoordinates) => void;
}

export interface MarkerCoordinates {
  lat?: number;
  lng?: number;
}

const MyMap: React.FC<MyMapProps> = ({ lat, lng, setCoordinates }) => {
  const mapRef = useRef<HTMLElement>(null);

  // const [mapCreated, setMapCreated] = useState<boolean>(false);
  const [marker, setMarker] = useState<MarkerCoordinates>({ lat, lng });

  let markerId = "";
  let mapCreated = false;

  useEffect(() => {
    let canceled = false;
    let googleMap: GoogleMap | null = null;

    createMap();
    mapCreated = true;
    return () => {
      canceled = true;
      googleMap?.removeAllMapListeners();
    };

    async function createMap() {
      if (!mapRef.current) {
        return;
      }
      googleMap = await GoogleMap.create({
        id: "my-cool-map",
        element: mapRef.current,
        apiKey: mapsApiKey,
        config: {
          center: { lat, lng },
          zoom: 8,
        },
      });

      if (markerId == "") {
        log("map not created yet");
        log("adding initial marker");
        const newMarkerId = await googleMap?.addMarker({
          coordinate: { lat, lng },
        });
        log(`initial marker id = ${newMarkerId}`);
        setCoordinates({
          lat,
          lng,
        });
        markerId = newMarkerId;
      }

      await googleMap.setOnMapClickListener(async ({ latitude, longitude }) => {
        log("map click");
        log("removing previous marker..");
        log(`previous markerId: ${markerId}`);
        if (markerId != "") {
          log("XDXDXDDXDX");
          await googleMap?.removeMarker(markerId);
          log("2xd");
        }
        log("adding new marker");
        const newMarkerId = await googleMap?.addMarker({
          coordinate: { lat: latitude, lng: longitude },
        });
        log(`new marker id =${newMarkerId}`);
        setCoordinates({
          lat: latitude,
          lng: longitude,
        });
        markerId = newMarkerId ? newMarkerId : "";
      });
    }
  }, [mapRef.current]);

  return (
    <div className="component-wrapper">
      <capacitor-google-map
        ref={mapRef}
        style={{
          display: "block",
          width: 300,
          height: 400,
        }}
      ></capacitor-google-map>
    </div>
  );
};

export default MyMap;
