const BASE_URL = import.meta.env.VITE_BASE_URL;

export const fetchCountries = async () => {
  const res = await fetch(`${BASE_URL}/countries`);
  if (!res.ok) throw new Error("Failed to fetch countries");
  return res.json();
};

export const fetchRegions = async (countryCode) => {
  const res = await fetch(`${BASE_URL}/countries/${countryCode}/regions`);
  if (!res.ok) throw new Error("Failed to fetch regions");
  return res.json();
};

export const fetchRiskData = async (regionId) => {
  const res = await fetch(`${BASE_URL}/risk/${regionId}`);
  if (!res.ok) throw new Error("Failed to fetch risk data");
  return res.json();
};

export const fetchAiExplanation = async (regionId) => {
  const res = await fetch(`${BASE_URL}/risk/${regionId}/explain`);
  if (!res.ok) throw new Error("Failed to fetch explanation");
  return res.json();
};
