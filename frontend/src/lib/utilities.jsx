import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

import countries from "i18n-iso-countries";
import en from "i18n-iso-countries/langs/en.json";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}


countries.registerLocale(en);

export const geocodeRegion = async (region, countryCode) => {
  try {
    const countryName = countries.getName(countryCode, "en");

    const query = encodeURIComponent(`${region}, ${countryName}`);

    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${query}`,
      {
        headers: {
          "User-Agent": "Eco-pulse",
        },
      },
    );

    const data = await res.json();

    if (data.length > 0) {
      return {
        lat: parseFloat(data[0].lat),
        lon: parseFloat(data[0].lon),
      };
    }

    return null;
  } catch (err) {
    console.error(err);
    return null;
  }
};