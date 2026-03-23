import { useNavigate } from "react-router-dom";
import Button from "../components/ReUsables/Button";
import RightArrow from "../assets/svgIcons/right-arrow.svg?react";
import { useState } from "react";
import { useCountries, useFloodAnalysis, useRegions } from "../hooks/APIHooks";
import routes from "../constants/routes";
import { HiChevronDown } from "react-icons/hi";
import lowIcon from "../assets/svgIcons/status-low-icon.png";
import moderateIcon from "../assets/svgIcons/status-moderate-icon.svg";
import highIcon from "../assets/svgIcons/status-high-icon.svg";
import { LuCloudHail } from "react-icons/lu";
import Map from "./Map";
import Modal from "../components/ReUsables/Modal";
import SignUp from "./SignUp";
import Loader from "../components/ReUsables/Loader";

const Landing = () => {
  const navigate = useNavigate();
  const [selectedCountry, setSelectedCountry] = useState("");
  const [selectedRegionId, setSelectedRegionId] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [email, setEmail] = useState("");
  const [openSignupModal, setOpenSignupModal] = useState(false);
  const [isOpeningModal, setIsOpeningModal] = useState(false);

  const { data: countryData } = useCountries();
  const { data: regionData } = useRegions(selectedCountry);
  const { riskQuery, aiQuery } = useFloodAnalysis(
    selectedRegionId,
    isSearching,
  );

  const getRiskStyles = (level) => {
    switch (level?.toLowerCase()) {
      case "low":
        return {
          border: "border-[#4CBB17]",
          bg: "bg-[#F8F8FF]",
          text: "text-[#4CBB17]",
          icon: lowIcon,
        };
      case "moderate":
        return {
          border: "border-[#FE5A1D]",
          bg: "bg-[#F8F8FF]",
          text: "text-[#FE5A1D]",
          icon: moderateIcon,
        };
      case "high":
        return {
          border: "border-[#CE2029]",
          bg: "bg-[#F8F8FF]",
          text: "text-red-600",
          icon: highIcon,
        };
      default:
        return {
          border: "border-gray-300",
          bg: "bg-gray-50",
          text: "text-gray-600",
          icon: "ℹ",
        };
    }
  };

  const isProcessing = riskQuery.isFetching || aiQuery.isFetching;

  const handleSearch = () => {
    if (selectedRegionId) {
      setIsSearching(true);
    }
  };

  return (
    <section className="">
      <section className="grid grid-cols-1 md:grid-cols-3">
        <div className="col-span-1 md:col-span-2 flex-1 relative z-0 h-125 md:h-full">
          <Map
            riskData={riskQuery.data ? [riskQuery.data] : []}
            selectedCountry={selectedCountry}
            aiQuery={aiQuery}
          />
        </div>
        <div className="col-span-1 bg-[#CDD8DFE5] py-5 px-2 lg:px-4 space-y-6">
          <h1 className="typo-2xl text-[#F8F8FF]">FLOOD RISK MAP</h1>

          <div className="bg-[#F8F8FFCC] rounded-xl p-3 space-y-3">
            <h4 className="text-xl font-medium">Map Key</h4>
            <div className="grid grid-cols-3 gap-2">
              {[
                { title: "High", backgroundColor: "#CE2029" },
                { title: "Moderate", backgroundColor: "#FE5A1D" },
                { title: "Low", backgroundColor: "#4CBB17" },
              ].map((item) => (
                <div
                  className="flex flex-col xl:flex-row gap-1 lg:gap-3 items-center"
                  key={item.title}
                >
                  <div
                    className="w-8 h-8 rounded-full"
                    style={{ backgroundColor: item.backgroundColor }}
                  />
                  <p className="typo-base">{item.title}</p>
                </div>
              ))}
            </div>
          </div>

          <section className="flood-risk-section bg-[#F8F8FFE5] rounded-xl p-4 space-y-6">
            <div className="relative w-full">
              <select
                value={selectedCountry}
                onChange={(e) => {
                  setSelectedCountry(e.target.value);
                  setIsSearching(false);
                }}
                className="form-input peer focus:outline-none transition-all appearance-none pr-10 cursor-pointer w-full"
              >
                <option value="" disabled hidden>
                  Select Country
                </option>
                {countryData?.countries.map((country) => (
                  <option key={country.code} value={country.code}>
                    {country.name}
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                <HiChevronDown className="h-5 w-5 text-gray-500" />
              </div>
            </div>

            <div className="relative w-full">
              <select
                value={selectedRegionId}
                onChange={(e) => {
                  setSelectedRegionId(e.target.value);
                  setIsSearching(false);
                }}
                className="form-input w-full appearance-none pr-10 cursor-pointer"
              >
                <option value="">Select Region</option>
                {regionData?.regions.map((r) => (
                  <option key={r.region_id} value={r.region_id}>
                    {r.region_name}
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-3 flex items-center pointer-events-none">
                <HiChevronDown className="h-5 w-5 text-gray-500" />
              </div>
            </div>

            <div className="flex justify-center ">
              <Button
                onClick={handleSearch}
                disabled={!selectedRegionId || isProcessing}
                className="btn btn-primary btn-md"
              >
                Check Flood Risk
              </Button>
            </div>
          </section>

          <div className="flex items-center gap-2">
            <LuCloudHail />
            <h4 className="text-sm">
              Flood risk is updated daily based on rainfall over the last 7
              days.
            </h4>
          </div>

          <div className="mt-4">
            {isProcessing ? (
              <div className="bg-white rounded-xl p-6 shadow-sm text-center space-y-4">
                <div className="flex justify-center">
                  <div className="animate-spin rounded-full h-10 w-10 border-4 border-[#63B7B9] border-t-transparent"></div>
                </div>
                <p className="text-gray-700 font-medium">
                  Analyzing recent rainfall and flood risk...
                </p>
                <p className="text-sm text-gray-500">
                  This usually takes just a few seconds
                </p>
              </div>
            ) : riskQuery.isError || aiQuery.isError ? (
              <div className="bg-[#F8F8FF] p-4 rounded-xl border border-[#296083] text-center space-y-3">
                <h4 className="typo-lg font-semibold">
                  Region Not Supported Yet
                </h4>
                <p className="typo-sm">
                  Flood risk data not available for this area right now.
                </p>
                <div className="flex justify-center gap-3">
                  <Button className="btn btn-accent btn-sm">
                    View Guidance
                  </Button>
                </div>
              </div>
            ) : riskQuery.data ? (
              <div className="rounded-xl bg-white p-6 shadow-sm text-center space-y-5">
                <div
                  className={`flex items-center justify-center space-x-3 rounded-xl p-3 border ${getRiskStyles(riskQuery.data.risk_level).border} ${getRiskStyles(riskQuery.data.risk_level).bg}`}
                >
                  <img
                    src={getRiskStyles(riskQuery.data.risk_level).icon}
                    alt={`${riskQuery.data.risk_level} risk icon`}
                    className="w-8 h-8 object-contain"
                  />
                  <div
                    className={`typo-xl font-bold ${getRiskStyles(riskQuery.data.risk_level).text}`}
                  >
                    {riskQuery.data.risk_level} Risk
                  </div>
                </div>

                <p className="text-sm text-gray-700 leading-relaxed">
                  {aiQuery.data?.explanation ||
                    "Rainfall and flood indicators have been analyzed for this area."}
                </p>

                <div>
                  <h1 className="text-sm font-medium text-[#9A9493]">
                    Updated {aiQuery.data?.valid_at || "recently"}
                  </h1>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-xl p-6 shadow-sm text-center space-y-4 opacity-80">
                <div className="flex justify-center items-center">
                  <LuCloudHail size={40} />
                </div>
                <h4 className="font-medium text-gray-700">
                  Select a region to check flood risk
                </h4>
                <p className="text-sm text-gray-500">
                  Choose a country and region above, then click "Check Flood
                  Risk" to see the latest analysis.
                </p>
              </div>
            )}
          </div>

          <div className="flex flex-col justify-center gap-4">
            <Button
              onClick={() => navigate(routes.main.resources())}
              className="btn btn-primary btn-md"
              rightSection={<RightArrow />}
            >
              Local Resources
            </Button>
            <Button
              onClick={() => navigate(routes.main.emergency())}
              className="btn btn-accent btn-md"
              rightSection={<RightArrow />}
            >
              Emergency Prep
            </Button>
          </div>
        </div>
      </section>

      {/* Newsletter / Alerts banner */}
      <section className="bg-[#63B7B9] py-12">
        <div className="site-container flex flex-col justify-center items-center gap-6 mx-auto px-4">
          <h1 className="text-[#F8F8FF] typo-2xl text-center">
            FLOOD ALERTS AND PREPAREDNESS YOU CAN TRUST ACROSS AFRICA
          </h1>

          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email to receive early flood warnings"
            className="w-full text-sm bg-white rounded-[20px] py-3 px-5"
            disabled={isOpeningModal}
          />

          <Button
            onClick={() => {
              if (!email) return;
              setIsOpeningModal(true);
              setOpenSignupModal(true);
              setTimeout(() => setIsOpeningModal(false), 800);
            }}
            rightSection={<RightArrow />}
            className="btn btn-primary btn-md"
          >
            Receive emergency flood alerts
          </Button>
        </div>
      </section>

      <Modal opened={openSignupModal} onClose={() => setOpenSignupModal(false)}>
        {isOpeningModal ? (
          <Loader />
        ) : (
          <SignUp
            onClose={() => setOpenSignupModal(false)}
            defaultEmail={email}
          />
        )}
      </Modal>
    </section>
  );
};

export default Landing;
