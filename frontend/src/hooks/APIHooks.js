import { useQuery } from "@tanstack/react-query";
import * as api from "../services/api"; 
import { locationKeys, riskKeys } from "./keys";

export const useCountries = () => {
  return useQuery({
    queryKey: locationKeys.countries(),
    queryFn: api.fetchCountries,
    staleTime: 1000 * 60 * 60,
  });
};

export const useRegions = (countryCode) => {
  return useQuery({
    queryKey: locationKeys.regions(countryCode),
    queryFn: () => api.fetchRegions(countryCode),
    enabled: !!countryCode,
  });
};

export const useFloodAnalysis = (regionId, enabled) => {
  const riskQuery = useQuery({
    queryKey: riskKeys.detail(regionId),
    queryFn: () => api.fetchRiskData(regionId),
    enabled: enabled && !!regionId,
  });

  const aiQuery = useQuery({
    queryKey: riskKeys.explanation(regionId),
    queryFn: () => api.fetchAiExplanation(regionId),
    enabled: enabled && !!regionId,
  });

  return { riskQuery, aiQuery };
};


