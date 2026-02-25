export const locationKeys = {
  all: ["locations"],
  countries: () => [...locationKeys.all, "countries"],
  regions: (countryCode) => [...locationKeys.all, "regions", countryCode],
};

export const riskKeys = {
  all: ["risk"],
  detail: (regionId) => [...riskKeys.all, "detail", regionId],
  explanation: (regionId) => [...riskKeys.all, "explanation", regionId],
};
