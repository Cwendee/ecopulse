import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Circle, Popup, useMap } from "react-leaflet";
import { geocodeRegion } from "../lib/utilities";

const riskColors = {
  high: "#CE2029",
  moderate: "#FE5A1D",
  low: "#4CBB17",
  unknown: "#888888",
};

const getColor = (level) =>
  riskColors[level?.toLowerCase()] || riskColors.unknown;

const getRadius = (level) => {
  switch (level?.toLowerCase()) {
    case "high":
      return 350000;
    case "moderate":
      return 250000;
    case "low":
      return 180000;
    default:
      return 120000;
  }
};

export function FloodRiskCircles({ riskData, aiQuery }) {
  const [coordsMap, setCoordsMap] = useState({});
  const [activeRegion, setActiveRegion] = useState(null);

  const regions = Array.isArray(riskData) ? riskData : [riskData];

  useEffect(() => {
    const fetchCoords = async () => {
      for (const item of regions) {
        const key = item.region_id || item.region_name;
        if (coordsMap[key]) continue;

        const coords = await geocodeRegion(item.region_name, item.country_code);
        if (coords) {
          setCoordsMap((prev) => ({ ...prev, [key]: coords }));
        }
      }
    };
    if (regions.length > 0) fetchCoords();
  }, [regions]);

  return (
    <>
      {regions.map((item) => {
        const key = item.region_id || item.region_name;
        const coords = coordsMap[key];
        if (!coords) return null;

        const level = item.risk_level || "unknown";
        const color = getColor(level);
        const radius = getRadius(level);

        return (
          <Circle
            key={key}
            center={[coords.lat, coords.lon]}
            radius={radius}
            pathOptions={{ color, fillColor: color, fillOpacity: 0.45, weight: 2 }}
            eventHandlers={{
              click: () => setActiveRegion(item),
            }}
          />
        );
      })}

      {activeRegion && coordsMap[activeRegion.region_id] && (
        <Popup
          position={[
            coordsMap[activeRegion.region_id].lat,
            coordsMap[activeRegion.region_id].lon,
          ]}
          onClose={() => setActiveRegion(null)}
          closeButton={true}
          closeOnClick={false}
        >
          <div className="p-0 lg:p-4 w-55 md:w-75">
            <p className="text-xs text-[#63B7B9] font-bold">
              Region: {activeRegion.region_name}
            </p>
            <p className="text-lg font-semibold">
              {activeRegion.risk_level.toUpperCase()} Risk
            </p>
            <p className="text-sm">
              {aiQuery?.data?.explanation || "No detailed explanation available"}
            </p>
            <p className="text-xs">
              Valid as of {activeRegion.valid_at || aiQuery?.data?.valid_at || "N/A"}
            </p>
          </div>
        </Popup>
      )}
    </>
  );
}

const MapController = ({ selectedCountry, riskData }) => {
  const map = useMap();

  useEffect(() => {
    if (!selectedCountry || !riskData) {
      map.setView(AFRICA_CENTER, INITIAL_ZOOM);
      return;
    }

    const region = Array.isArray(riskData) ? riskData[0] : riskData;
    if (region?.lat && region?.lon) {
      map.setView([region.lat, region.lon], 6); // zoom in
    }
  }, [selectedCountry, riskData, map]);

  return null;
};


const AFRICA_CENTER = [0, 20];
const INITIAL_ZOOM = 3;

export default function Map({ riskData, selectedCountry, aiQuery }) {
  return (
    <MapContainer
      center={AFRICA_CENTER}
      zoom={INITIAL_ZOOM}
      scrollWheelZoom={true}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapController selectedCountry={selectedCountry} riskData={riskData} />
      {riskData && <FloodRiskCircles riskData={riskData} aiQuery={aiQuery} />}
    </MapContainer>
  );
}
